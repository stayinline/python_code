import weaviate
from weaviate.collections.classes.config import Configure
from weaviate.connect import ConnectionParams
from weaviate.classes.config import DataType

import ollama

# ================================
# 0. 使用 Ollama embedding
# ================================
def embed(text: str):
    response = ollama.embeddings(
        model="nomic-embed-text",
        prompt=text
    )
    return response["embedding"]

# ================================
# 1. 连接 Weaviate
# ================================
client = weaviate.WeaviateClient(
    connection_params=ConnectionParams.from_url(
        "http://192.168.1.131:18080",
        grpc_port=50051
    )
)

client.connect()

# ================================
# 2. 检查服务状态
# ================================
if client.is_ready():
    print("Weaviate is ready ✅")
else:
    raise Exception("Weaviate is not ready ❌")

# ================================
# 3. 删除旧 Collection
# ================================
try:
    client.collections.delete("Article")
    print("Deleted existing 'Article'")
except:
    print("No existing 'Article'")

# ================================
# 4. 创建 Collection（不使用向量化）
# ================================
client.collections.create(
    name="Article",
    properties=[
        {"name": "title", "data_type": DataType.TEXT},
        {"name": "content", "data_type": DataType.TEXT}
    ]
)


print("Collection 'Article' created ✅")

# ================================
# 5. 插入数据（Ollama embedding）
# ================================
articles = [
    {"title": "Hello World", "content": "This is the first article about vectors."},
    {"title": "Weaviate Demo", "content": "Weaviate is a vector database for semantic search."},
    {"title": "Python Integration", "content": "You can use Python client to insert and query vectors."}
]

article_collection = client.collections.get("Article")

for article in articles:
    text = article["title"] + " " + article["content"]
    vector = embed(text)

    print(f"vector dim = {len(vector)}")  # 🔍 验证

    article_collection.data.insert(
        properties=article,
        vector=vector
    )

print("Inserted sample articles ✅")

# ================================
# 6. 普通查询
# ================================
print("\n=== Fetch Objects ===")
result = article_collection.query.fetch_objects()

for item in result.objects:
    print(f"- {item.properties['title']}")

# ================================
# 7. 验证向量
# ================================
print("\n=== Check Vectors ===")
result_with_vector = article_collection.query.fetch_objects(
    include_vector=True
)

for obj in result_with_vector.objects:
    vector = obj.vector["default"]
    print(f"{obj.properties['title']} -> vector dim: {len(vector)}")
# ================================
# 8. 语义搜索
# ================================
print("\n=== Semantic Search (near_vector) ===")

query_text = "vector database"
query_vector = embed(query_text)

search_result = article_collection.query.near_vector(
    near_vector=query_vector,
    limit=2
)

for item in search_result.objects:
    print(f"- {item.properties['title']}: {item.properties['content']}")

# ================================
# 9. 关闭连接
# ================================
client.close()
print("\nDone ✅")