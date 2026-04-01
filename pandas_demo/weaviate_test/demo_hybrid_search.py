"""
Weaviate Hybrid Search（混合搜索）完整演示
==========================================
场景：电商平台商品搜索

核心对比（为什么需要 Hybrid Search）：
┌─────────────────┬──────────────────────────────┬─────────────────────────────┐
│   搜索方式        │         优点                  │         缺点                │
├─────────────────┼──────────────────────────────┼─────────────────────────────┤
│ MySQL LIKE      │ 精确匹配                       │ 不理解语义，无法匹配同义词    │
│ ES / BM25       │ TF-IDF 词频统计，关键词匹配好  │ 语义理解弱，无法跨语言      │
│ 纯向量搜索       │ 语义理解强，能匹配意思相近内容  │ 对精确关键词/型号不敏感      │
│ Hybrid Search   │ 结合 BM25 + 向量，取两者之长   │ 需要调优 alpha 参数          │
└─────────────────┴──────────────────────────────┴─────────────────────────────┘

演示内容：
  1. 数据准备：商品库入库（BM25 索引 + 向量索引同时建立）
  2. 关键词搜索的盲区（纯 BM25 失败案例）
  3. 纯向量搜索的盲区（语义漂移，精确词不敏感）
  4. Hybrid Search：两者结合
  5. alpha 参数调优（0.0 ~ 1.0 连续变化对比）
  6. fusion_type 对比（rankedFusion vs relativeScoreFusion）
  7. Hybrid + Filter 联合查询
  8. 多语言查询（中文问英文商品）

技术栈：Weaviate v4 + Ollama (nomic-embed-text)
"""

import logging
import sys
import time
from dataclasses import dataclass, field
from typing import Optional

import ollama
import weaviate
from weaviate.classes.config import DataType, Property
from weaviate.classes.query import Filter, HybridFusion, MetadataQuery
from weaviate.collections.classes.config import Configure
from weaviate.connect import ConnectionParams

# ================================================================
# 配置 & 日志
# ================================================================
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s - %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger("HybridSearchDemo")

WEAVIATE_HOST  = "http://192.168.1.131:18080"
GRPC_PORT      = 50051
EMBED_MODEL    = "nomic-embed-text"
COLLECTION     = "Product"


# ================================================================
# 商品数据
# ================================================================
@dataclass
class Product:
    name: str          # 商品名称
    description: str   # 描述（供语义向量化）
    category: str      # 分类
    brand: str         # 品牌
    price: float       # 价格
    tags: str          # 标签（逗号分隔）
    vector: list = field(default_factory=list, repr=False)


# 精心设计的商品库 —— 覆盖"纯关键词"和"纯语义"各自的盲区
PRODUCTS = [
    # ── 数码 ──────────────────────────────────────────────────────
    Product(
        name="Sony WH-1000XM5 无线降噪耳机",
        description="行业领先主动降噪，30小时长续航，多点蓝牙连接，折叠便携设计，适合商务出行和专注工作",
        category="数码", brand="Sony", price=2499.0,
        tags="耳机,降噪,蓝牙,Sony,无线"
    ),
    Product(
        name="Apple AirPods Pro 第二代",
        description="自适应主动降噪，通透模式，H2芯片，个性化空间音频，MagSafe充电盒，苹果生态首选",
        category="数码", brand="Apple", price=1899.0,
        tags="耳机,AirPods,降噪,Apple,无线"
    ),
    Product(
        name="BOSE QuietComfort 45",
        description="经典商务降噪耳机，轻盈舒适佩戴，安静模式与通透模式切换，适合长途飞行旅行",
        category="数码", brand="BOSE", price=2299.0,
        tags="耳机,降噪,BOSE,旅行,舒适"
    ),
    Product(
        name="Logitech MX Master 3S 无线鼠标",
        description="8000 DPI高精度传感器，电磁滚轮，人体工学设计，支持多设备切换，程序员和设计师神器",
        category="数码", brand="Logitech", price=699.0,
        tags="鼠标,无线,人体工学,办公,Logitech"
    ),
    Product(
        name="Keychron K2 机械键盘",
        description="75%紧凑布局，支持Mac/Windows，红轴线性触感，铝合金外壳，RGB背光，Type-C有线无线双模",
        category="数码", brand="Keychron", price=599.0,
        tags="键盘,机械键盘,无线,Mac,办公"
    ),
    Product(
        name="iPad Pro 12.9寸 M2芯片",
        description="M2超强性能，Liquid Retina XDR屏幕，雷雳4接口，支持Apple Pencil和妙控键盘，专业创作平板",
        category="数码", brand="Apple", price=8999.0,
        tags="平板,iPad,Apple,M2,创作"
    ),
    Product(
        name="Samsung 三星 T7 移动固态硬盘 1TB",
        description="USB 3.2 Gen2接口，读速1050MB/s，金属外壳防震，支持指纹加密，轻巧便携随身存储",
        category="数码", brand="Samsung", price=399.0,
        tags="硬盘,移动硬盘,固态,Samsung,存储"
    ),

    # ── 家居 ──────────────────────────────────────────────────────
    Product(
        name="Dyson V15 Detect 无绳吸尘器",
        description="激光显尘技术，LCD实时显示灰尘数量，HEPA过滤99.97%微尘，60分钟续航，适合宠物家庭",
        category="家居", brand="Dyson", price=4990.0,
        tags="吸尘器,无线,Dyson,宠物,清洁"
    ),
    Product(
        name="小米空气净化器 4 Pro",
        description="OLED触屏显示，支持PM2.5/甲醛实时检测，HEPA+活性炭双层过滤，米家APP智能控制，适合新房除甲醛",
        category="家居", brand="小米", price=1299.0,
        tags="空气净化,小米,甲醛,PM2.5,智能家居"
    ),
    Product(
        name="Philips 飞利浦 HX9954 电动牙刷",
        description="声波震动技术，62000次/分钟，5种清洁模式，压力感应保护牙龈，蓝牙连接智慧洁净APP",
        category="家居", brand="Philips", price=899.0,
        tags="牙刷,电动牙刷,Philips,口腔护理,蓝牙"
    ),
    Product(
        name="美的（Midea）变频空调挂机 1.5匹",
        description="一级能效变频省电，WiFi智控，新一级能效，自清洁功能，制冷制热双效，适合15-22平方米卧室",
        category="家居", brand="美的", price=2699.0,
        tags="空调,变频,美的,节能,智能家居"
    ),

    # ── 运动 ──────────────────────────────────────────────────────
    Product(
        name="Nike Air Zoom Pegasus 40 跑鞋",
        description="React泡棉中底提供回弹缓震，Zoom气垫前掌加速，透气飞织鞋面，适合日常训练和长距离跑步",
        category="运动", brand="Nike", price=899.0,
        tags="跑鞋,Nike,跑步,训练,缓震"
    ),
    Product(
        name="Garmin Forerunner 265 跑步手表",
        description="AMOLED彩屏，跑步动态指标，血氧心率监测，13天续航，Race Widget预测完赛时间，专业跑者首选",
        category="运动", brand="Garmin", price=2888.0,
        tags="手表,运动手表,Garmin,跑步,GPS"
    ),
    Product(
        name="Keep 瑜伽垫 天然橡胶 5mm",
        description="双面防滑天然橡胶，无毒环保材质，5mm厚度关节保护，背包带携带方便，适合瑜伽普拉提拉伸",
        category="运动", brand="Keep", price=199.0,
        tags="瑜伽垫,瑜伽,Keep,健身,防滑"
    ),

    # ── 办公 ──────────────────────────────────────────────────────
    Product(
        name="Herman Miller Aeron 人体工学椅",
        description="PostureFit SL背部支撑，8Z Pellicle悬挂式坐垫，全方位调节，久坐不疲劳，程序员/设计师必备",
        category="办公", brand="Herman Miller", price=12800.0,
        tags="椅子,人体工学,办公椅,久坐,程序员"
    ),
    Product(
        name="乐歌 E5 电动升降桌 双电机",
        description="双电机静音升降，记忆高度一键还原，防夹手安全保护，承重100kg，适合站立办公改善久坐健康",
        category="办公", brand="乐歌", price=2199.0,
        tags="升降桌,站立办公,乐歌,办公,人体工学"
    ),
    Product(
        name="BenQ ScreenBar 屏幕挂灯",
        description="自动感光调节，无眩光无频闪，不占桌面空间，USB供电，色温2700-6500K可调，护眼编程灯",
        category="办公", brand="BenQ", price=399.0,
        tags="台灯,挂灯,护眼,BenQ,办公,编程"
    ),
]


# ================================================================
# 工具函数
# ================================================================

def embed(text: str) -> list[float]:
    response = ollama.embeddings(model=EMBED_MODEL, prompt=text)
    return response["embedding"]


def setup_collection(client: weaviate.WeaviateClient):
    """
    创建商品集合。
    关键：同时开启 BM25 索引（默认开启）和向量索引 —— 这是 Hybrid Search 的基础。
    Weaviate 会为每个对象同时维护：
      ① 倒排索引（用于 BM25 关键词匹配）
      ② 向量索引（HNSW，用于向量近邻搜索）
    """
    if client.collections.exists(COLLECTION):
        client.collections.delete(COLLECTION)
        logger.info("已删除旧 Collection: %s", COLLECTION)

    client.collections.create(
        name=COLLECTION,
        vectorizer_config=Configure.Vectorizer.none(),   # 手动管理向量
        properties=[
            Property(name="name",        data_type=DataType.TEXT),
            Property(name="description", data_type=DataType.TEXT),
            Property(name="category",    data_type=DataType.TEXT),
            Property(name="brand",       data_type=DataType.TEXT),
            Property(name="price",       data_type=DataType.NUMBER),
            Property(name="tags",        data_type=DataType.TEXT),
        ]
    )
    logger.info("Collection '%s' 创建成功（BM25倒排索引 + HNSW向量索引）", COLLECTION)


def bulk_insert(client: weaviate.WeaviateClient):
    col = client.collections.get(COLLECTION)
    logger.info("开始批量写入 %d 条商品数据...", len(PRODUCTS))

    with col.batch.dynamic() as batch:
        for p in PRODUCTS:
            # 向量化：商品名 + 描述 + 标签（语义内容尽量完整）
            vector = embed(f"{p.name} {p.description} {p.tags}")
            batch.add_object(
                properties={
                    "name":        p.name,
                    "description": p.description,
                    "category":    p.category,
                    "brand":       p.brand,
                    "price":       p.price,
                    "tags":        p.tags,
                },
                vector=vector
            )

    total = col.aggregate.over_all(total_count=True).total_count
    logger.info("写入完成，商品总数: %d", total)


def print_results(results, title: str, show_score: bool = True, limit: int = 5):
    """格式化打印搜索结果"""
    print(f"\n  {'─'*65}")
    print(f"  {title}")
    print(f"  {'─'*65}")

    objects = results.objects[:limit]
    if not objects:
        print("  (无结果)")
        return

    for i, obj in enumerate(objects, 1):
        p = obj.properties
        score_str = ""
        if show_score and obj.metadata:
            score_parts = []
            if obj.metadata.score is not None:
                score_parts.append(f"hybrid={obj.metadata.score:.4f}")
            if obj.metadata.explain_score:
                # explain_score 包含 BM25 和向量各自的得分详情
                score_parts.append(f"explain={obj.metadata.explain_score[:80]}...")
            score_str = f"  [{', '.join(score_parts)}]"
        print(f"  [{i}] {p['name']}")
        print(f"       品牌:{p['brand']}  分类:{p['category']}  价格:¥{p['price']:.0f}")
        if score_str:
            print(f"      {score_str}")


# ================================================================
# 演示 1：关键词搜索的盲区
# ================================================================

def demo1_bm25_blind_spot(col):
    """
    BM25（关键词）搜索的局限性演示。
    查询"隔音耳机"——商品库里没有"隔音"这个词，都叫"降噪"，BM25 会漏掉。

    对比 MySQL LIKE 查询：
      SELECT * FROM products WHERE name LIKE '%隔音%' OR description LIKE '%隔音%'
      → 0条结果（因为用词不同）
    """
    logger.info("=" * 70)
    logger.info("Demo 1: BM25 关键词搜索盲区 — 同义词无法匹配")

    print("""
  背景：用户搜索「隔音耳机」
  商品库中实际用的词是「降噪耳机」（ANC / 主动降噪）
  ─────────────────────────────────────────────────────
  MySQL LIKE 等效：
    SELECT * FROM products
    WHERE name LIKE '%隔音%' OR description LIKE '%隔音%'
  → 结果：0 条（字面无匹配）
  ─────────────────────────────────────────────────────""")

    result_bm25 = col.query.bm25(
        query="隔音耳机",
        limit=5,
        return_metadata=MetadataQuery(score=True)
    )
    print_results(result_bm25, "BM25 关键词搜索「隔音耳机」结果：", show_score=False)
    if not result_bm25.objects:
        print("  ⚠ BM25 结果为空 —— 因为商品库无「隔音」字样，只有「降噪」")

    result_vector = col.query.near_vector(
        near_vector=embed("隔音耳机"),
        limit=5,
        return_metadata=MetadataQuery(distance=True)
    )
    print(f"\n  {'─'*65}")
    print(f"  纯向量搜索「隔音耳机」结果（语义理解同义词）：")
    print(f"  {'─'*65}")
    for i, obj in enumerate(result_vector.objects, 1):
        p = obj.properties
        dist = obj.metadata.distance if obj.metadata else "?"
        print(f"  [{i}] {p['name']}  (distance={dist:.4f})")
    print("  ✓ 向量搜索能理解「隔音」≈「降噪」，正确召回相关商品")


# ================================================================
# 演示 2：纯向量搜索的盲区
# ================================================================

def demo2_vector_blind_spot(col):
    """
    纯向量搜索对精确型号/品牌名不敏感。
    查询「WH-1000XM5」（精确型号），向量搜索可能召回无关商品。

    类比：ES 中 match query vs term query 的区别。
    """
    logger.info("=" * 70)
    logger.info("Demo 2: 纯向量搜索盲区 — 精确型号/品牌名匹配不稳定")

    print("""
  背景：用户搜索精确型号「WH-1000XM5」
  纯语义向量对产品编号语义稀薄，可能无法精准排在第一
  ─────────────────────────────────────────────────────""")

    result_vector = col.query.near_vector(
        near_vector=embed("WH-1000XM5"),
        limit=5,
        return_metadata=MetadataQuery(distance=True)
    )
    print(f"\n  纯向量搜索「WH-1000XM5」结果：")
    for i, obj in enumerate(result_vector.objects, 1):
        p = obj.properties
        dist = obj.metadata.distance if obj.metadata else "?"
        marker = " ← ✓ 目标商品" if "WH-1000XM5" in p["name"] else ""
        print(f"  [{i}] {p['name']}  (distance={dist:.4f}){marker}")

    result_bm25 = col.query.bm25(
        query="WH-1000XM5",
        limit=5,
        return_metadata=MetadataQuery(score=True)
    )
    print(f"\n  BM25 搜索「WH-1000XM5」结果：")
    for i, obj in enumerate(result_bm25.objects, 1):
        p = obj.properties
        score = obj.metadata.score if obj.metadata else "?"
        marker = " ← ✓ 目标商品" if "WH-1000XM5" in p["name"] else ""
        print(f"  [{i}] {p['name']}  (score={score:.4f}){marker}")
    print("  ✓ BM25 能精确匹配型号字符串")


# ================================================================
# 演示 3：Hybrid Search 登场
# ================================================================

def demo3_hybrid_basic(col):
    """
    Hybrid Search = BM25 + 向量搜索的融合（Reciprocal Rank Fusion）。

    内部机制：
      1. 分别运行 BM25 和向量搜索，各取 TopK 候选集
      2. 按 Reciprocal Rank Fusion 公式融合排名：
         RRF_score = Σ (1 / (rank_i + 60))
      3. 按融合得分重新排序返回

    alpha 参数控制权重：
      alpha=0.0 → 纯 BM25（等价于关键词搜索）
      alpha=0.5 → BM25 与向量各半（默认）
      alpha=1.0 → 纯向量搜索
    """
    logger.info("=" * 70)
    logger.info("Demo 3: Hybrid Search 基础使用")

    queries = [
        ("隔音耳机",    "语义词，库中无精确词「隔音」，只有「降噪」"),
        ("WH-1000XM5", "精确型号，考验关键词精确匹配能力"),
        ("程序员工作必备", "模糊意图，需要语义理解"),
        ("健身房运动装备", "品类模糊，考验语义泛化能力"),
    ]

    for query, note in queries:
        result = col.query.hybrid(
            query=query,
            vector=embed(query),                # Vectorizer.none() 时必须手动传入查询向量
            alpha=0.5,                          # 默认平衡权重
            fusion_type=HybridFusion.RANKED,    # Reciprocal Rank Fusion
            limit=3,
            return_metadata=MetadataQuery(score=True)
        )
        print(f"\n  查询: 「{query}」  ({note})")
        print(f"  {'─'*60}")
        for i, obj in enumerate(result.objects, 1):
            p = obj.properties
            score = obj.metadata.score if obj.metadata else "?"
            print(f"  [{i}] {p['name']}")
            print(f"       ¥{p['price']:.0f}  {p['brand']}  score={score:.4f}")


# ================================================================
# 演示 4：alpha 参数调优
# ================================================================

def demo4_alpha_tuning(col):
    """
    通过同一查询，展示 alpha 从 0.0 到 1.0 的变化如何影响结果排序。

    实际业务调优建议：
      - 精确商品搜索（含型号/品牌）   → alpha ≈ 0.25（偏 BM25）
      - 意图/场景类搜索              → alpha ≈ 0.75（偏向量）
      - 通用搜索框                   → alpha = 0.5（默认平衡）
    """
    logger.info("=" * 70)
    logger.info("Demo 4: alpha 参数调优对比（0.0 → 1.0）")

    query = "安静专注工作的耳机"  # 偏语义意图，无精确关键词
    alphas = [0.0, 0.25, 0.5, 0.75, 1.0]
    labels = {
        0.0:  "纯 BM25 （等价 ES 关键词搜索）",
        0.25: "偏 BM25  （关键词为主 + 少量语义）",
        0.5:  "平衡     （Hybrid 默认）",
        0.75: "偏向量   （语义为主 + 少量关键词）",
        1.0:  "纯向量   （等价语义搜索）",
    }

    print(f"\n  查询: 「{query}」")
    print(f"  {'─'*70}")
    print(f"  {'alpha':<6} {'模式':<30} 第1名")
    print(f"  {'─'*70}")

    query_vector = embed(query)
    for alpha in alphas:
        result = col.query.hybrid(
            query=query,
            vector=query_vector,
            alpha=alpha,
            limit=1,
            return_metadata=MetadataQuery(score=True)
        )
        top1 = result.objects[0].properties["name"] if result.objects else "(无结果)"
        score = result.objects[0].metadata.score if result.objects and result.objects[0].metadata else 0
        print(f"  {alpha:<6} {labels[alpha]:<32} {top1}  ({score:.4f})")

    # 详细对比：alpha=0.0 vs alpha=1.0 的完整 Top3
    print(f"\n  详细对比：alpha=0.0（纯BM25）vs alpha=1.0（纯向量）")
    for alpha in [0.0, 1.0]:
        result = col.query.hybrid(
            query=query,
            vector=query_vector,
            alpha=alpha,
            limit=3,
            return_metadata=MetadataQuery(score=True)
        )
        mode = "纯BM25" if alpha == 0.0 else "纯向量"
        print(f"\n  [{mode}] alpha={alpha}")
        for i, obj in enumerate(result.objects, 1):
            p = obj.properties
            print(f"    [{i}] {p['name']}  ¥{p['price']:.0f}")


# ================================================================
# 演示 5：fusion_type 对比
# ================================================================

def demo5_fusion_type(col):
    """
    Weaviate 支持两种 Hybrid 融合算法：

    1. HybridFusion.RANKED（默认，Reciprocal Rank Fusion）
       公式：score = Σ 1/(rank + 60)
       特点：只看排名，不看原始分数；对极端分数不敏感；稳定

    2. HybridFusion.RELATIVE_SCORE
       公式：score = α × norm(vector_score) + (1-α) × norm(bm25_score)
       特点：对原始分数做归一化后加权；分数差异越大影响越显著；更灵活

    何时选哪种：
      - RANKED：大多数场景默认推荐，结果稳定
      - RELATIVE_SCORE：需要 score 有实际业务含义时（如相关度阈值过滤）
    """
    logger.info("=" * 70)
    logger.info("Demo 5: fusion_type 对比（RANKED vs RELATIVE_SCORE）")

    query = "长途出行旅行的降噪耳机"

    print(f"\n  查询: 「{query}」  (alpha=0.5)\n")
    print(f"  {'─'*65}")
    print(f"  {'排名':<4} {'RANKED (RRF)':<38} {'RELATIVE_SCORE'}")
    print(f"  {'─'*65}")

    query_vector = embed(query)
    result_ranked = col.query.hybrid(
        query=query,
        vector=query_vector,
        alpha=0.5,
        fusion_type=HybridFusion.RANKED,
        limit=5,
        return_metadata=MetadataQuery(score=True)
    )

    result_relative = col.query.hybrid(
        query=query,
        vector=query_vector,
        alpha=0.5,
        fusion_type=HybridFusion.RELATIVE_SCORE,
        limit=5,
        return_metadata=MetadataQuery(score=True)
    )

    max_len = max(len(result_ranked.objects), len(result_relative.objects))
    for i in range(max_len):
        r_name = r_score = rs_name = rs_score = ""
        if i < len(result_ranked.objects):
            p = result_ranked.objects[i].properties
            r_score = result_ranked.objects[i].metadata.score or 0
            r_name = f"{p['name'][:28]} ({r_score:.4f})"
        if i < len(result_relative.objects):
            p = result_relative.objects[i].properties
            rs_score = result_relative.objects[i].metadata.score or 0
            rs_name = f"{p['name'][:28]} ({rs_score:.4f})"
        print(f"  [{i+1}]  {r_name:<40} {rs_name}")


# ================================================================
# 演示 6：Hybrid + Filter 联合查询
# ================================================================

def demo6_hybrid_with_filter(col):
    """
    Hybrid Search 与过滤条件结合：
    先用 Filter 缩小候选集（精确过滤），再在候选集内做混合搜索。

    等价于 ES 的：
      bool query:
        filter: [category=数码, price<=3000]
        should: [match(name), knn(vector)]

    对比 MySQL：只能做过滤 + 关键词，无法语义搜索
    """
    logger.info("=" * 70)
    logger.info("Demo 6: Hybrid + Filter 联合查询")

    scenarios = [
        {
            "label":  "数码类 + 价格 ≤ ¥1000",
            "query":  "无线音乐设备",
            "filter": Filter.all_of([
                Filter.by_property("category").equal("数码"),
                Filter.by_property("price").less_or_equal(1000)
            ])
        },
        {
            "label":  "Apple 品牌商品",
            "query":  "移动办公生产力工具",
            "filter": Filter.by_property("brand").equal("Apple")
        },
        {
            "label":  "运动 & 家居类（非数码）",
            "query":  "健康生活方式相关产品",
            "filter": Filter.any_of([
                Filter.by_property("category").equal("运动"),
                Filter.by_property("category").equal("家居"),
            ])
        },
    ]

    for s in scenarios:
        result = col.query.hybrid(
            query=s["query"],
            vector=embed(s["query"]),
            alpha=0.6,
            filters=s["filter"],
            limit=3,
            return_metadata=MetadataQuery(score=True)
        )
        print(f"\n  ┌─ 过滤条件: {s['label']}")
        print(f"  │  查询意图: 「{s['query']}」")
        print(f"  │  {'─'*55}")
        for i, obj in enumerate(result.objects, 1):
            p = obj.properties
            score = obj.metadata.score if obj.metadata else "?"
            print(f"  │  [{i}] {p['name']}")
            print(f"  │      {p['brand']} / {p['category']} / ¥{p['price']:.0f}  score={score:.4f}")
        print(f"  └{'─'*58}")


# ================================================================
# 演示 7：多语言查询（中文查英文商品）
# ================================================================

def demo7_multilingual(col):
    """
    向量模型（nomic-embed-text）具备多语言语义能力。
    BM25 无法跨语言（字面不匹配），但 Hybrid 中的向量部分可以弥补。

    场景：用中文描述查询英文/混合语言商品名称。
    """
    logger.info("=" * 70)
    logger.info("Demo 7: 多语言查询 — 中文意图查英文商品名")

    queries = [
        "noise cancelling headphone for travel",
        "ergonomic office chair for programmer",
        "mechanical keyboard for coding",
    ]

    print(f"\n  英文查询 → 中英混合商品库")
    print(f"  （BM25 字面匹配失败，向量跨语言语义弥补）\n")

    for query in queries:
        result_bm25 = col.query.bm25(query=query, limit=1)
        result_hybrid = col.query.hybrid(
            query=query,
            vector=embed(query),
            alpha=0.7,
            limit=1,
            return_metadata=MetadataQuery(score=True)
        )

        bm25_top = result_bm25.objects[0].properties["name"] if result_bm25.objects else "(无匹配)"
        hybrid_top = result_hybrid.objects[0].properties["name"] if result_hybrid.objects else "(无匹配)"
        h_score = result_hybrid.objects[0].metadata.score if result_hybrid.objects and result_hybrid.objects[0].metadata else 0

        print(f"  查询: 「{query}」")
        print(f"    BM25   → {bm25_top}")
        print(f"    Hybrid → {hybrid_top}  (score={h_score:.4f})")
        print()


# ================================================================
# 演示 8：Explain Score（得分解释）
# ================================================================

def demo8_explain_score(col):
    """
    explain_score 返回 BM25 和向量各自的贡献，帮助调试和理解排名原因。
    类似 ES 的 _explain API。
    """
    logger.info("=" * 70)
    logger.info("Demo 8: explain_score — 理解 Hybrid 排名是如何计算的")

    result = col.query.hybrid(
        query="蓝牙降噪耳机",
        vector=embed("蓝牙降噪耳机"),
        alpha=0.5,
        limit=2,
        return_metadata=MetadataQuery(score=True, explain_score=True)
    )

    print(f"\n  查询: 「蓝牙降噪耳机」  alpha=0.5")
    print(f"  {'─'*65}")
    for i, obj in enumerate(result.objects, 1):
        p = obj.properties
        score = obj.metadata.score if obj.metadata else "?"
        explain = obj.metadata.explain_score if obj.metadata else ""
        print(f"\n  [{i}] {p['name']}")
        print(f"       hybrid score = {score:.6f}")
        print(f"       得分解释:")
        # explain_score 是一段文字描述，按换行拆开打印
        for line in (explain or "").split(";"):
            line = line.strip()
            if line:
                print(f"         • {line}")


# ================================================================
# 对比总结
# ================================================================

def print_comparison_summary():
    print("""
╔══════════════════════════════════════════════════════════════════════════╗
║                   搜索方式对比总结                                        ║
╠══════════╦═══════════════════╦═══════════════════╦════════════════════════╣
║ 搜索方式  ║  精确型号/品牌     ║  同义词/语义意图   ║  跨语言查询             ║
╠══════════╬═══════════════════╬═══════════════════╬════════════════════════╣
║ MySQL    ║ LIKE ✓ (字面匹配) ║ ✗ 完全失败        ║ ✗                     ║
║ ES BM25  ║ ✓ (TF-IDF加权)   ║ △ 需要同义词表    ║ ✗                     ║
║ 纯向量   ║ △ 型号语义稀薄     ║ ✓✓ 强            ║ ✓ (多语言模型)        ║
║ Hybrid   ║ ✓ (BM25补充)     ║ ✓✓ (向量补充)    ║ ✓ (向量部分生效)      ║
╠══════════╬═══════════════════╩═══════════════════╩════════════════════════╣
║ 推荐场景  ║ 电商搜索 / 企业知识库 / 代码搜索 / 多语言内容检索               ║
╚══════════╩═════════════════════════════════════════════════════════════════╝

  alpha 选择建议：
    0.0        → 完全关键词（等价 ES BM25）
    0.25       → 以关键词为主，适合型号/SKU搜索
    0.5        → 默认平衡，通用搜索框推荐
    0.75       → 以语义为主，适合意图/场景搜索
    1.0        → 完全语义（等价 near_vector）
""")


# ================================================================
# 主程序
# ================================================================

def main():
    logger.info("Weaviate Hybrid Search 演示启动")

    client = weaviate.WeaviateClient(
        connection_params=ConnectionParams.from_url(
            WEAVIATE_HOST,
            grpc_port=GRPC_PORT
        )
    )

    try:
        client.connect()
        if not client.is_ready():
            raise RuntimeError("Weaviate 服务不可用，请检查服务状态")
        logger.info("Weaviate 连接成功")

        # ── 初始化数据 ────────────────────────────────────────────
        setup_collection(client)
        bulk_insert(client)
        time.sleep(0.5)   # 等待索引就绪

        col = client.collections.get(COLLECTION)

        # ── 演示系列 ───────────────────────────────────────────────
        demo1_bm25_blind_spot(col)
        demo2_vector_blind_spot(col)
        demo3_hybrid_basic(col)
        demo4_alpha_tuning(col)
        demo5_fusion_type(col)
        demo6_hybrid_with_filter(col)
        demo7_multilingual(col)
        demo8_explain_score(col)

        print_comparison_summary()

    finally:
        client.close()
        logger.info("连接已关闭")


if __name__ == "__main__":
    main()
