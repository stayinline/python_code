"""
企业知识库语义检索系统 (Enterprise Knowledge Base - Semantic Search)
===================================================================
场景：企业内部将技术文档、FAQ、产品手册统一入库，
      支持语义搜索、分类过滤、混合查询，供员工和客服快速检索。

技术栈：Weaviate + Ollama (nomic-embed-text)
"""

import logging
import sys
from dataclasses import dataclass, field
from typing import Optional
import weaviate
from weaviate.collections.classes.config import Configure
from weaviate.connect import ConnectionParams
from weaviate.classes.config import DataType, Property
from weaviate.classes.query import MetadataQuery
import ollama

# ================================================================
# 日志配置
# ================================================================
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s - %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger("KnowledgeBase")


# ================================================================
# 配置类
# ================================================================
@dataclass
class WeaviateConfig:
    host: str = "http://192.168.1.131:18080"
    grpc_port: int = 50051
    collection_name: str = "KnowledgeArticle"
    embed_model: str = "nomic-embed-text"


# ================================================================
# 数据模型
# ================================================================
@dataclass
class KnowledgeArticle:
    title: str
    content: str
    category: str          # 分类：技术文档 / 产品手册 / FAQ / 政策规定
    department: str        # 所属部门：研发 / 运维 / 产品 / 客服
    tags: str              # 标签（逗号分隔）
    author: str
    version: str = "1.0"
    vector: list = field(default_factory=list, repr=False)


# ================================================================
# 企业知识库服务
# ================================================================
class KnowledgeBaseService:
    """
    企业知识库核心服务：
    - 管理 Weaviate Collection 生命周期
    - 使用 Ollama 生成语义向量
    - 支持批量写入、语义检索、混合查询、分类过滤
    """

    def __init__(self, config: WeaviateConfig):
        self.config = config
        self.client: Optional[weaviate.WeaviateClient] = None
        self.collection = None

    # ----------------------------------------------------------------
    # 连接管理（支持 with 语法）
    # ----------------------------------------------------------------
    def __enter__(self):
        self._connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._disconnect()

    def _connect(self):
        logger.info("正在连接 Weaviate: %s", self.config.host)
        self.client = weaviate.WeaviateClient(
            connection_params=ConnectionParams.from_url(
                self.config.host,
                grpc_port=self.config.grpc_port
            )
        )
        self.client.connect()
        if not self.client.is_ready():
            raise RuntimeError("Weaviate 服务不可用，请检查服务状态")
        logger.info("Weaviate 连接成功")

    def _disconnect(self):
        if self.client:
            self.client.close()
            logger.info("Weaviate 连接已关闭")

    # ----------------------------------------------------------------
    # Collection 初始化
    # ----------------------------------------------------------------
    def init_collection(self, force_recreate: bool = False):
        name = self.config.collection_name

        if force_recreate and self.client.collections.exists(name):
            self.client.collections.delete(name)
            logger.info("已删除旧 Collection: %s", name)

        if not self.client.collections.exists(name):
            self.client.collections.create(
                name=name,
                properties=[
                    Property(name="title",      data_type=DataType.TEXT),
                    Property(name="content",    data_type=DataType.TEXT),
                    Property(name="category",   data_type=DataType.TEXT),
                    Property(name="department", data_type=DataType.TEXT),
                    Property(name="tags",       data_type=DataType.TEXT),
                    Property(name="author",     data_type=DataType.TEXT),
                    Property(name="version",    data_type=DataType.TEXT),
                ],
                # 不使用 Weaviate 内置向量化器，由本服务手动管理向量
                vectorizer_config=Configure.Vectorizer.none()
            )
            logger.info("Collection '%s' 创建成功", name)
        else:
            logger.info("Collection '%s' 已存在，跳过创建", name)

        self.collection = self.client.collections.get(name)

    # ----------------------------------------------------------------
    # Embedding
    # ----------------------------------------------------------------
    def embed(self, text: str) -> list[float]:
        response = ollama.embeddings(model=self.config.embed_model, prompt=text)
        return response["embedding"]

    # ----------------------------------------------------------------
    # 批量写入
    # ----------------------------------------------------------------
    def bulk_insert(self, articles: list[KnowledgeArticle]):
        logger.info("开始批量写入，共 %d 条文档", len(articles))
        success, failed = 0, 0

        with self.collection.batch.dynamic() as batch:
            for article in articles:
                try:
                    # 拼接语义化文本（title + content + tags 联合 embed）
                    embed_text = f"{article.title} {article.tags} {article.content}"
                    vector = self.embed(embed_text)

                    batch.add_object(
                        properties={
                            "title":      article.title,
                            "content":    article.content,
                            "category":   article.category,
                            "department": article.department,
                            "tags":       article.tags,
                            "author":     article.author,
                            "version":    article.version,
                        },
                        vector=vector
                    )
                    success += 1
                    logger.debug("写入: %s", article.title)
                except Exception as e:
                    failed += 1
                    logger.error("写入失败 [%s]: %s", article.title, e)

        logger.info("批量写入完成：成功 %d / 失败 %d", success, failed)

    # ----------------------------------------------------------------
    # 语义检索（near_vector）
    # ----------------------------------------------------------------
    def semantic_search(
        self,
        query: str,
        limit: int = 5,
        category: Optional[str] = None,
        department: Optional[str] = None
    ) -> list[dict]:
        """
        语义向量检索，支持按 category / department 过滤
        """
        query_vector = self.embed(query)

        filters = self._build_filters(category, department)

        result = self.collection.query.near_vector(
            near_vector=query_vector,
            limit=limit,
            filters=filters,
            return_metadata=MetadataQuery(distance=True)
        )

        return self._format_results(result.objects, include_distance=True)

    # ----------------------------------------------------------------
    # 关键词过滤查询（fetch_objects + where filter）
    # ----------------------------------------------------------------
    def filter_by_category(self, category: str, limit: int = 10) -> list[dict]:
        """按分类精确查询"""
        from weaviate.classes.query import Filter

        result = self.collection.query.fetch_objects(
            filters=Filter.by_property("category").equal(category),
            limit=limit
        )
        return self._format_results(result.objects)

    # ----------------------------------------------------------------
    # 统计各分类数量
    # ----------------------------------------------------------------
    def get_stats(self) -> dict:
        result = self.collection.aggregate.over_all(total_count=True)
        return {"total_count": result.total_count}

    # ----------------------------------------------------------------
    # 工具方法
    # ----------------------------------------------------------------
    def _build_filters(self, category: Optional[str], department: Optional[str]):
        from weaviate.classes.query import Filter

        conditions = []
        if category:
            conditions.append(Filter.by_property("category").equal(category))
        if department:
            conditions.append(Filter.by_property("department").equal(department))

        if len(conditions) == 0:
            return None
        if len(conditions) == 1:
            return conditions[0]
        return Filter.all_of(conditions)

    def _format_results(self, objects, include_distance: bool = False) -> list[dict]:
        results = []
        for obj in objects:
            p = obj.properties
            item = {
                "title":      p.get("title"),
                "category":   p.get("category"),
                "department": p.get("department"),
                "tags":       p.get("tags"),
                "author":     p.get("author"),
                "content":    p.get("content", "")[:120] + "...",
            }
            if include_distance and obj.metadata:
                item["distance"] = round(obj.metadata.distance, 4)
            results.append(item)
        return results


# ================================================================
# 企业示例数据
# ================================================================
SAMPLE_ARTICLES = [
    KnowledgeArticle(
        title="Kubernetes 集群部署最佳实践",
        content="本文介绍在生产环境中部署 Kubernetes 集群的标准流程，包括节点规划、网络插件选型（Calico/Flannel）、"
                "存储类配置、RBAC 权限模型、HPA 弹性伸缩策略，以及监控告警体系（Prometheus + Grafana）的集成方式。",
        category="技术文档",
        department="运维",
        tags="kubernetes,k8s,容器,部署,运维",
        author="张工"
    ),
    KnowledgeArticle(
        title="微服务熔断与限流设计规范",
        content="基于 Sentinel 实现微服务熔断降级与流量控制，涵盖：QPS 限流、并发线程数限流、慢调用比例熔断、"
                "异常比例熔断，以及热点参数限流。配置中心使用 Nacos，实现动态规则推送。",
        category="技术文档",
        department="研发",
        tags="微服务,熔断,限流,sentinel,nacos",
        author="李工"
    ),
    KnowledgeArticle(
        title="数据库慢查询排查手册",
        content="MySQL 慢查询排查流程：开启 slow_query_log，设置 long_query_time=1s，使用 pt-query-digest 分析慢日志，"
                "结合 EXPLAIN 分析执行计划，重点关注 Full Table Scan、Using filesort、Using temporary 等问题索引优化方向。",
        category="技术文档",
        department="研发",
        tags="mysql,数据库,慢查询,性能优化,索引",
        author="王工"
    ),
    KnowledgeArticle(
        title="员工报销流程说明",
        content="差旅费及日常办公报销须在费用发生后 15 个工作日内提交，通过 OA 系统填写报销单，附发票原件。"
                "单笔超过 5000 元需部门总监审批，超过 2 万元需 CFO 审批。财务每周五统一打款。",
        category="政策规定",
        department="财务",
        tags="报销,差旅,财务,OA,审批流",
        author="HR部门"
    ),
    KnowledgeArticle(
        title="新员工入职 IT 配置指南",
        content="入职当天联系 IT 部门领取设备，提供工号激活企业邮箱。VPN 使用 GlobalProtect，"
                "配置文件从内网下载。开发环境使用标准镜像（Ubuntu 22.04 / Windows 11），"
                "代码托管在私有 GitLab，权限申请通过工单系统提交。",
        category="FAQ",
        department="IT",
        tags="入职,IT,VPN,邮箱,开发环境",
        author="IT部门"
    ),
    KnowledgeArticle(
        title="智能客服产品使用手册 v2.3",
        content="智能客服系统支持多渠道接入（Web/App/微信/400电话），内置意图识别引擎，准确率 > 92%。"
                "知识库管理支持 Excel 批量导入，支持富文本回答、图片、视频卡片。"
                "人工坐席支持会话转接、实时辅助、质检回放功能。SLA 响应时间 < 3 秒。",
        category="产品手册",
        department="产品",
        tags="智能客服,知识库,意图识别,SLA,多渠道",
        author="产品团队"
    ),
    KnowledgeArticle(
        title="CI/CD 流水线配置规范",
        content="使用 GitLab CI + ArgoCD 实现 GitOps 发布流程。流水线阶段：代码检查（SonarQube）→ 单元测试 → "
                "镜像构建（Kaniko）→ 漏洞扫描（Trivy）→ 推送镜像仓库 → ArgoCD 自动同步。"
                "生产发布需手动触发，并填写变更单号。",
        category="技术文档",
        department="运维",
        tags="CI/CD,GitLab,ArgoCD,GitOps,流水线,发布",
        author="DevOps团队"
    ),
    KnowledgeArticle(
        title="如何申请云资源（AWS/阿里云）",
        content="云资源申请通过内部云管平台提交工单，填写业务说明、预计用量、成本中心编号。"
                "测试环境资源 1 个工作日内审批完成，生产环境需架构评审，3 个工作日内完成。"
                "资源到期前 7 天系统自动提醒，不续期将自动释放。",
        category="FAQ",
        department="运维",
        tags="云资源,AWS,阿里云,申请流程,工单",
        author="云平台团队"
    ),
]


# ================================================================
# 主程序
# ================================================================
def main():
    config = WeaviateConfig()

    with KnowledgeBaseService(config) as svc:

        # 1. 初始化 Collection（强制重建，演示用）
        logger.info("=" * 60)
        logger.info("Step 1: 初始化知识库 Collection")
        svc.init_collection(force_recreate=True)

        # 2. 批量写入企业文档
        logger.info("=" * 60)
        logger.info("Step 2: 写入企业知识文档")
        svc.bulk_insert(SAMPLE_ARTICLES)

        # 3. 统计
        logger.info("=" * 60)
        stats = svc.get_stats()
        logger.info("知识库统计: 总文档数 = %d", stats["total_count"])

        # 4. 语义检索示例
        queries = [
            ("容器化部署和集群管理", None, None),
            ("数据库性能问题怎么排查", None, "研发"),
            ("员工费用怎么报销", "政策规定", None),
            ("how to set up VPN for new employee", "FAQ", None),
        ]

        logger.info("=" * 60)
        logger.info("Step 3: 语义检索演示")

        for query, cat, dept in queries:
            print(f"\n{'─'*60}")
            print(f"  查询: {query}")
            if cat:
                print(f"  过滤: category={cat}")
            if dept:
                print(f"  过滤: department={dept}")
            print(f"{'─'*60}")

            results = svc.semantic_search(query, limit=3, category=cat, department=dept)

            if not results:
                print("  (无结果)")
            for i, r in enumerate(results, 1):
                print(f"  [{i}] [{r['distance']}] {r['title']}")
                print(f"       分类: {r['category']}  部门: {r['department']}  作者: {r['author']}")
                print(f"       标签: {r['tags']}")
                print(f"       摘要: {r['content']}")

        # 5. 按分类精确过滤
        logger.info("=" * 60)
        logger.info("Step 4: 按分类过滤 - '技术文档'")
        tech_docs = svc.filter_by_category("技术文档")
        for doc in tech_docs:
            print(f"  - [{doc['department']}] {doc['title']}")

    logger.info("=" * 60)
    logger.info("企业知识库演示完成")


if __name__ == "__main__":
    main()
