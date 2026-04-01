"""
Weaviate Cross-References (交叉引用) 完整演示
================================================
场景：技术博客系统
    - BlogAuthor  博主/作者
    - BlogTag     文章标签
    - BlogPost    博文 → 引用 BlogAuthor（多对一） + BlogTag（多对多）

演示内容：
    1. 定义含跨集合引用的 Schema
    2. 插入各集合基础数据
    3. 批量添加引用关系（正向引用）
    4. 查询时展开引用（return_references）
    5. 多级引用：通过文章查作者再查其他文章
    6. 反向引用：通过 Author 查出其所有文章
    7. 引用 + 过滤条件联合查询
    8. 动态更新引用（修改文章作者）
    9. 删除单条引用
   10. 汇总统计（聚合 + 引用计数）

技术栈：Weaviate v4 Python Client（无向量化，纯引用关系演示）
"""

import logging
import sys
import uuid
from dataclasses import dataclass

import weaviate
from weaviate.classes.config import Property, DataType, ReferenceProperty
from weaviate.classes.query import Filter, QueryReference
from weaviate.collections.classes.config import Configure
from weaviate.connect import ConnectionParams

# ================================================================
# 日志配置
# ================================================================
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s - %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger("CrossRefDemo")

WEAVIATE_HOST = "http://192.168.1.131:18080"
GRPC_PORT = 50051

# Collection 名称常量
COL_AUTHOR = "BlogAuthor"
COL_TAG = "BlogTag"
COL_POST = "BlogPost"


# ================================================================
# Schema 定义
# ================================================================

def setup_schema(client: weaviate.WeaviateClient):
    """
    创建三个 Collection，BlogPost 通过 ReferenceProperty 引用 BlogAuthor 和 BlogTag。

    引用关系图：
        BlogPost ──hasTags──────► BlogTag   (多对多)
        BlogPost ──writtenBy────► BlogAuthor (多对一)
    """
    logger.info("=" * 60)
    logger.info("Step 1: 初始化 Schema（含 Cross-Reference 属性）")

    # 先删除旧 Collection（演示用，保证幂等）
    for name in [COL_POST, COL_AUTHOR, COL_TAG]:
        if client.collections.exists(name):
            client.collections.delete(name)
            logger.info("  已删除旧 Collection: %s", name)

    # ── 1. BlogAuthor ─────────────────────────────────────────────
    client.collections.create(
        name=COL_AUTHOR,
        vectorizer_config=Configure.Vectorizer.none(),
        properties=[
            Property(name="name",       data_type=DataType.TEXT),
            Property(name="email",      data_type=DataType.TEXT),
            Property(name="department", data_type=DataType.TEXT),
            Property(name="bio",        data_type=DataType.TEXT),
        ]
    )
    logger.info("  ✓ Collection '%s' 创建成功", COL_AUTHOR)

    # ── 2. BlogTag ────────────────────────────────────────────────
    client.collections.create(
        name=COL_TAG,
        vectorizer_config=Configure.Vectorizer.none(),
        properties=[
            Property(name="name",        data_type=DataType.TEXT),
            Property(name="description", data_type=DataType.TEXT),
            Property(name="color",       data_type=DataType.TEXT),
        ]
    )
    logger.info("  ✓ Collection '%s' 创建成功", COL_TAG)

    # ── 3. BlogPost（含 Cross-Reference 属性）─────────────────────
    # 注意：ReferenceProperty 必须通过单独的 references 参数传入，
    #       不能混在 properties 列表中（Weaviate v4 限制）
    client.collections.create(
        name=COL_POST,
        vectorizer_config=Configure.Vectorizer.none(),
        properties=[
            Property(name="title",     data_type=DataType.TEXT),
            Property(name="content",   data_type=DataType.TEXT),
            Property(name="status",    data_type=DataType.TEXT),   # draft / published
            Property(name="viewCount", data_type=DataType.INT),
        ],
        references=[
            # 多对一：每篇博文有一个作者
            ReferenceProperty(
                name="writtenBy",
                target_collection=COL_AUTHOR
            ),
            # 多对多：每篇博文可以有多个标签
            ReferenceProperty(
                name="hasTags",
                target_collection=COL_TAG
            ),
        ]
    )
    logger.info("  ✓ Collection '%s' 创建成功（含 writtenBy → %s, hasTags → %s）",
                COL_POST, COL_AUTHOR, COL_TAG)


# ================================================================
# 插入数据
# ================================================================

def insert_data(client: weaviate.WeaviateClient) -> dict:
    """
    插入作者、标签、博文，返回各对象的 UUID 字典
    """
    logger.info("=" * 60)
    logger.info("Step 2: 插入基础数据（Author / Tag / Post）")

    authors_col = client.collections.get(COL_AUTHOR)
    tags_col    = client.collections.get(COL_TAG)
    posts_col   = client.collections.get(COL_POST)

    # ── 插入作者 ─────────────────────────────────────────────────
    author_uuids = {}
    author_data = [
        {"name": "张工",   "email": "zhang@example.com", "department": "后端研发", "bio": "10年Java经验，专注微服务架构"},
        {"name": "李工",   "email": "li@example.com",    "department": "前端研发", "bio": "Vue/React全栈，专注工程化"},
        {"name": "王工",   "email": "wang@example.com",  "department": "运维",     "bio": "DevOps专家，K8s认证工程师"},
        {"name": "陈工",   "email": "chen@example.com",  "department": "数据",     "bio": "大数据/AI算法工程师"},
    ]
    for a in author_data:
        uid = authors_col.data.insert(properties=a)
        author_uuids[a["name"]] = uid
        logger.info("  插入 Author: %-6s → %s", a["name"], uid)

    # ── 插入标签 ─────────────────────────────────────────────────
    tag_uuids = {}
    tag_data = [
        {"name": "Java",       "description": "Java生态技术",        "color": "#b07219"},
        {"name": "Kubernetes", "description": "容器编排平台",         "color": "#326ce5"},
        {"name": "MySQL",      "description": "关系型数据库",         "color": "#4479A1"},
        {"name": "Vue",        "description": "前端渐进式框架",       "color": "#42b883"},
        {"name": "微服务",      "description": "分布式服务架构",      "color": "#ff6b6b"},
        {"name": "性能优化",    "description": "系统性能调优",        "color": "#ffd93d"},
        {"name": "CI/CD",      "description": "持续集成与持续部署",   "color": "#fc6d26"},
        {"name": "大数据",      "description": "分布式数据处理",      "color": "#e25d33"},
    ]
    for t in tag_data:
        uid = tags_col.data.insert(properties=t)
        tag_uuids[t["name"]] = uid
        logger.info("  插入 Tag:    %-10s → %s", t["name"], uid)

    # ── 插入博文（先不加引用，之后单独添加） ─────────────────────
    post_uuids = {}
    post_data = [
        {
            "title": "Spring Boot 微服务最佳实践",
            "content": "本文深入讲解 Spring Boot 微服务的核心实践，包括服务注册发现（Nacos）、配置中心、熔断降级（Sentinel）、链路追踪（SkyWalking）等完整技术栈。",
            "status": "published",
            "viewCount": 3200,
        },
        {
            "title": "MySQL 索引原理与慢查询优化",
            "content": "从 InnoDB B+Tree 索引结构出发，详解联合索引最左前缀、覆盖索引、索引下推等优化手段，结合 pt-query-digest 实战慢查询分析。",
            "status": "published",
            "viewCount": 5100,
        },
        {
            "title": "Kubernetes 生产级部署实战",
            "content": "手把手演示 K8s 多节点集群搭建，包括 Calico 网络插件、Ceph 持久化存储、HPA 弹性伸缩、PodDisruptionBudget 滚动升级，以及 Prometheus+Grafana 监控全套。",
            "status": "published",
            "viewCount": 4400,
        },
        {
            "title": "Vue 3 Composition API 深度解析",
            "content": "系统梳理 Vue 3 Composition API 的设计动机，对比 Options API，重点演示 setup、ref/reactive、computed、watchEffect、provide/inject 以及自定义 Hooks 的最佳实践。",
            "status": "published",
            "viewCount": 2800,
        },
        {
            "title": "GitLab CI/CD + ArgoCD 全链路 GitOps",
            "content": "从代码提交到生产部署，演示 GitLab CI 流水线（lint→test→build→scan）与 ArgoCD 自动同步的完整 GitOps 工作流，附真实 .gitlab-ci.yml 配置。",
            "status": "published",
            "viewCount": 3600,
        },
        {
            "title": "大数据实时处理：Flink + Kafka 架构",
            "content": "基于 Apache Flink 1.17 实现实时风控场景，Kafka 作为数据总线，Flink SQL 处理流批一体，结合 RocksDB State Backend 实现高吞吐低延迟的实时计算管道。",
            "status": "draft",
            "viewCount": 0,
        },
        {
            "title": "JVM 性能调优完全指南",
            "content": "深入 JVM 内存模型（堆/栈/方法区），详解 G1/ZGC 垃圾回收器参数调优，借助 JFR、Async-Profiler、MAT 工具分析内存泄漏与 CPU 热点，附典型案例。",
            "status": "published",
            "viewCount": 2100,
        },
    ]
    for p in post_data:
        uid = posts_col.data.insert(properties=p)
        post_uuids[p["title"]] = uid
        logger.info("  插入 Post:   %s → %s", p["title"][:30], uid)

    return {"authors": author_uuids, "tags": tag_uuids, "posts": post_uuids}


# ================================================================
# 添加 Cross-References
# ================================================================

def add_references(client: weaviate.WeaviateClient, uuids: dict):
    """
    批量建立 BlogPost → BlogAuthor 和 BlogPost → BlogTag 的引用关系。
    使用 batch 方式高效写入。
    """
    logger.info("=" * 60)
    logger.info("Step 3: 批量添加 Cross-Reference 引用关系")

    posts_col = client.collections.get(COL_POST)
    authors = uuids["authors"]
    tags    = uuids["tags"]
    posts   = uuids["posts"]

    # 引用映射表：文章标题 → (作者, [标签列表])
    ref_map = {
        "Spring Boot 微服务最佳实践":         ("张工", ["Java", "微服务", "性能优化"]),
        "MySQL 索引原理与慢查询优化":          ("张工", ["MySQL", "性能优化"]),
        "Kubernetes 生产级部署实战":           ("王工", ["Kubernetes", "CI/CD"]),
        "Vue 3 Composition API 深度解析":      ("李工", ["Vue"]),
        "GitLab CI/CD + ArgoCD 全链路 GitOps": ("王工", ["CI/CD", "Kubernetes"]),
        "大数据实时处理：Flink + Kafka 架构":   ("陈工", ["大数据", "性能优化"]),
        "JVM 性能调优完全指南":                ("张工", ["Java", "性能优化"]),
    }

    with posts_col.batch.dynamic() as batch:
        for title, (author_name, tag_names) in ref_map.items():
            post_uid   = posts[title]
            author_uid = authors[author_name]

            # 添加 writtenBy 引用（多对一）
            batch.add_reference(
                from_uuid=post_uid,
                from_property="writtenBy",
                to=author_uid,
            )

            # 添加 hasTags 引用（多对多，每个标签一条引用）
            for tag_name in tag_names:
                batch.add_reference(
                    from_uuid=post_uid,
                    from_property="hasTags",
                    to=tags[tag_name],
                )

            logger.info(
                "  %-35s → 作者: %-4s | 标签: %s",
                title[:35], author_name, ", ".join(tag_names)
            )

    logger.info("Cross-Reference 引用关系添加完成")


# ================================================================
# 查询演示
# ================================================================

def demo_query_with_refs(client: weaviate.WeaviateClient):
    """
    演示 1：正向引用展开查询
    查询所有已发布博文，同时返回其作者信息和所有标签。
    """
    logger.info("=" * 60)
    logger.info("Demo 1: 正向引用查询 — 获取博文时展开作者 & 标签")

    posts_col = client.collections.get(COL_POST)

    result = posts_col.query.fetch_objects(
        filters=Filter.by_property("status").equal("published"),
        limit=10,
        # return_references 指定要展开的引用字段
        return_references=[
            QueryReference(
                link_on="writtenBy",
                return_properties=["name", "department"],   # 只拉取作者的指定字段
            ),
            QueryReference(
                link_on="hasTags",
                return_properties=["name", "color"],
            ),
        ]
    )

    print(f"\n{'─'*70}")
    print(f"  {'博文标题':<36} {'作者':<8} {'部门':<8} 标签")
    print(f"{'─'*70}")
    for obj in result.objects:
        p = obj.properties

        # 解析作者引用（多对一，取第一个）
        author_name = author_dept = "—"
        if obj.references and "writtenBy" in obj.references:
            author_objs = obj.references["writtenBy"].objects
            if author_objs:
                author_name = author_objs[0].properties.get("name", "—")
                author_dept = author_objs[0].properties.get("department", "—")

        # 解析标签引用（多对多）
        tag_names = []
        if obj.references and "hasTags" in obj.references:
            tag_names = [
                t.properties.get("name", "") for t in obj.references["hasTags"].objects
            ]

        print(f"  {p['title']:<36} {author_name:<8} {author_dept:<10} {', '.join(tag_names)}")


def demo_filter_by_referenced_prop(client: weaviate.WeaviateClient, uuids: dict):
    """
    演示 2：按引用对象的属性过滤
    查询指定作者（张工）写的所有博文。
    """
    logger.info("=" * 60)
    logger.info("Demo 2: 按引用属性过滤 — 查询「张工」的所有博文")

    posts_col  = client.collections.get(COL_POST)
    zhang_uuid = uuids["authors"]["张工"]

    # 通过引用目标的 UUID 精确过滤
    result = posts_col.query.fetch_objects(
        filters=Filter.by_ref("writtenBy").by_id().equal(zhang_uuid),
        return_references=[
            QueryReference(link_on="writtenBy", return_properties=["name"]),
            QueryReference(link_on="hasTags",   return_properties=["name"]),
        ]
    )

    print(f"\n  张工的博文（共 {len(result.objects)} 篇）：")
    for obj in result.objects:
        tag_names = []
        if obj.references and "hasTags" in obj.references:
            tag_names = [t.properties["name"] for t in obj.references["hasTags"].objects]
        print(f"    - {obj.properties['title']}")
        print(f"      标签: {', '.join(tag_names)}  | 阅读量: {obj.properties['viewCount']}")


def demo_filter_by_tag_name(client: weaviate.WeaviateClient):
    """
    演示 3：按引用对象的字段值过滤
    查询包含「性能优化」标签的所有博文。
    """
    logger.info("=" * 60)
    logger.info("Demo 3: 按引用属性值过滤 — 查询包含「性能优化」标签的博文")

    posts_col = client.collections.get(COL_POST)

    result = posts_col.query.fetch_objects(
        # by_ref(...).by_property(...) 实现"通过引用链过滤"
        filters=Filter.by_ref("hasTags").by_property("name").equal("性能优化"),
        return_references=[
            QueryReference(link_on="writtenBy", return_properties=["name"]),
            QueryReference(link_on="hasTags",   return_properties=["name"]),
        ]
    )

    print(f"\n  包含「性能优化」标签的博文（共 {len(result.objects)} 篇）：")
    for obj in result.objects:
        p = obj.properties
        author_name = "—"
        if obj.references and "writtenBy" in obj.references:
            refs = obj.references["writtenBy"].objects
            if refs:
                author_name = refs[0].properties.get("name", "—")
        tag_names = []
        if obj.references and "hasTags" in obj.references:
            tag_names = [t.properties["name"] for t in obj.references["hasTags"].objects]
        print(f"    - {p['title']}")
        print(f"      作者: {author_name}  标签: {', '.join(tag_names)}")


def demo_reverse_reference(client: weaviate.WeaviateClient, uuids: dict):
    """
    演示 4：反向引用查询（通过 Author 找到其所有博文）
    Weaviate v4 通过在 Author 端手动查询实现反向引用。
    """
    logger.info("=" * 60)
    logger.info("Demo 4: 反向引用 — 通过 Author 查询其所有博文")

    posts_col = client.collections.get(COL_POST)

    print(f"\n  各作者博文统计：")
    for author_name, author_uuid in uuids["authors"].items():
        result = posts_col.query.fetch_objects(
            filters=Filter.by_ref("writtenBy").by_id().equal(author_uuid),
            limit=10,
        )
        titles = [obj.properties["title"] for obj in result.objects]
        total_views = sum(obj.properties.get("viewCount", 0) for obj in result.objects)
        print(f"\n  ┌─ {author_name}（{len(titles)} 篇文章，总阅读量 {total_views}）")
        for t in titles:
            print(f"  │   • {t}")


def demo_update_reference(client: weaviate.WeaviateClient, uuids: dict):
    """
    演示 5：动态更新引用
    将「MySQL 索引原理与慢查询优化」的作者从「张工」改为「王工」
    操作步骤：先删除旧引用 → 添加新引用
    """
    logger.info("=" * 60)
    logger.info("Demo 5: 动态更新引用 — 修改文章作者")

    posts_col = client.collections.get(COL_POST)

    post_uuid   = uuids["posts"]["MySQL 索引原理与慢查询优化"]
    old_author  = uuids["authors"]["张工"]
    new_author  = uuids["authors"]["王工"]

    print(f"\n  操作：将「MySQL 索引原理与慢查询优化」的作者从「张工」改为「王工」")

    # 删除旧引用
    posts_col.data.reference_delete(
        from_uuid=post_uuid,
        from_property="writtenBy",
        to=old_author,
    )
    logger.info("  已删除旧引用（张工）")

    # 添加新引用
    posts_col.data.reference_add(
        from_uuid=post_uuid,
        from_property="writtenBy",
        to=new_author,
    )
    logger.info("  已添加新引用（王工）")

    # 验证结果
    updated = posts_col.query.fetch_object_by_id(
        uuid=post_uuid,
        return_references=[
            QueryReference(link_on="writtenBy", return_properties=["name", "department"]),
        ]
    )
    if updated and updated.references and "writtenBy" in updated.references:
        new_author_obj = updated.references["writtenBy"].objects
        if new_author_obj:
            a = new_author_obj[0].properties
            print(f"  验证结果：当前作者 = {a['name']} ({a['department']}) ✓")


def demo_add_tag_to_post(client: weaviate.WeaviateClient, uuids: dict):
    """
    演示 6：动态添加引用（为博文新增标签）
    给「Vue 3 Composition API 深度解析」添加「性能优化」标签
    """
    logger.info("=" * 60)
    logger.info("Demo 6: 动态添加引用 — 为博文新增标签")

    posts_col = client.collections.get(COL_POST)

    post_uuid = uuids["posts"]["Vue 3 Composition API 深度解析"]
    tag_uuid  = uuids["tags"]["性能优化"]

    print(f"\n  操作：给「Vue 3 Composition API 深度解析」添加「性能优化」标签")

    # 添加新引用（reference_add 支持重复调用，等幂）
    posts_col.data.reference_add(
        from_uuid=post_uuid,
        from_property="hasTags",
        to=tag_uuid,
    )

    # 验证结果
    updated = posts_col.query.fetch_object_by_id(
        uuid=post_uuid,
        return_references=[
            QueryReference(link_on="hasTags", return_properties=["name"]),
        ]
    )
    tags_now = []
    if updated and updated.references and "hasTags" in updated.references:
        tags_now = [t.properties["name"] for t in updated.references["hasTags"].objects]

    print(f"  当前标签：{', '.join(tags_now)} ✓")


def demo_replace_all_refs(client: weaviate.WeaviateClient, uuids: dict):
    """
    演示 7：一次性替换所有引用（reference_replace）
    将「Kubernetes 生产级部署实战」的标签集合整体替换
    """
    logger.info("=" * 60)
    logger.info("Demo 7: 整体替换引用集合（reference_replace）")

    posts_col = client.collections.get(COL_POST)
    post_uuid = uuids["posts"]["Kubernetes 生产级部署实战"]

    old_tags_result = posts_col.query.fetch_object_by_id(
        uuid=post_uuid,
        return_references=[QueryReference(link_on="hasTags", return_properties=["name"])]
    )
    old_tags = []
    if old_tags_result and old_tags_result.references and "hasTags" in old_tags_result.references:
        old_tags = [t.properties["name"] for t in old_tags_result.references["hasTags"].objects]

    new_tag_names = ["Kubernetes", "微服务", "性能优化"]
    new_tag_uuids = [uuids["tags"][n] for n in new_tag_names]

    print(f"\n  文章：「Kubernetes 生产级部署实战」")
    print(f"  旧标签：{', '.join(old_tags)}")
    print(f"  新标签：{', '.join(new_tag_names)}")

    # reference_replace 会删除所有旧引用，替换为新的引用列表
    posts_col.data.reference_replace(
        from_uuid=post_uuid,
        from_property="hasTags",
        to=new_tag_uuids,
    )

    # 验证
    updated = posts_col.query.fetch_object_by_id(
        uuid=post_uuid,
        return_references=[QueryReference(link_on="hasTags", return_properties=["name"])]
    )
    new_tags = []
    if updated and updated.references and "hasTags" in updated.references:
        new_tags = [t.properties["name"] for t in updated.references["hasTags"].objects]
    print(f"  替换后标签：{', '.join(new_tags)} ✓")


def demo_aggregate_with_ref(client: weaviate.WeaviateClient):
    """
    演示 8：聚合统计 + 引用结合
    统计各状态下博文数量、总阅读量
    """
    logger.info("=" * 60)
    logger.info("Demo 8: 聚合统计 — 各状态博文数量 & 阅读量")

    posts_col = client.collections.get(COL_POST)

    for status in ["published", "draft"]:
        result = posts_col.aggregate.over_all(
            filters=Filter.by_property("status").equal(status),
            total_count=True,
        )
        # 查出阅读量求和
        objs = posts_col.query.fetch_objects(
            filters=Filter.by_property("status").equal(status),
            limit=100,
        )
        total_views = sum(o.properties.get("viewCount", 0) for o in objs.objects)

        print(f"\n  状态: {status}")
        print(f"    文章数: {result.total_count}")
        print(f"    总阅读量: {total_views:,}")


# ================================================================
# 主程序
# ================================================================

def main():
    logger.info("Weaviate Cross-References 演示启动")
    logger.info("连接: %s (gRPC port: %d)", WEAVIATE_HOST, GRPC_PORT)

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
        logger.info("Weaviate 连接成功，版本: %s", client.get_meta().get("version", "unknown"))

        # ── Schema & 数据初始化 ─────────────────────────────────
        setup_schema(client)
        uuids = insert_data(client)
        add_references(client, uuids)

        # ── 查询演示 ────────────────────────────────────────────
        demo_query_with_refs(client)
        demo_filter_by_referenced_prop(client, uuids)
        demo_filter_by_tag_name(client)
        demo_reverse_reference(client, uuids)

        # ── 变更演示 ────────────────────────────────────────────
        demo_update_reference(client, uuids)
        demo_add_tag_to_post(client, uuids)
        demo_replace_all_refs(client, uuids)

        # ── 聚合统计 ────────────────────────────────────────────
        demo_aggregate_with_ref(client)

        logger.info("=" * 60)
        logger.info("Cross-References 演示全部完成！")

    finally:
        client.close()
        logger.info("连接已关闭")


if __name__ == "__main__":
    main()
