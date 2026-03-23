"""
依赖：pip install requests
Ollama 需本地运行并已拉取 embedding 模型，例如：
    ollama pull nomic-embed-text
"""

import requests

OLLAMA_URL   = "http://localhost:11434/api/embeddings"
OLLAMA_MODEL = "nomic-embed-text"   # 768 维，与 semantic_vector 匹配

CK_HTTP_URL = "http://192.168.1.124:8123"
CK_USER     = "default"
CK_PASSWORD = "65e84be3"
CK_TABLE    = "dwd_plant_health_detail_vector_v2"


def embed(text: str) -> list[float]:
    """用 Ollama 将文本编码为向量。"""
    resp = requests.post(OLLAMA_URL, json={"model": OLLAMA_MODEL, "prompt": text})
    resp.raise_for_status()
    return resp.json()["embedding"]


def query(question: str, top_k: int = 5) -> list[dict]:
    """向量化问题，在 ClickHouse 中做相似度检索，返回 top_k 条记录。"""
    vec = embed(question)
    vec_literal = "[" + ",".join(f"{v:.6f}" for v in vec) + "]"

    sql = f"""
    SELECT
        greenhouse_id,
        formatDateTime(ts, '%Y-%m-%d %H:%M:%S') AS ts,
        growth_stage,
        plant_height_cm,
        health_score,
        disease_risk,
        pest_risk,
        issue_type,
        temperature,
        humidity,
        soil_ph,
        text_desc,
        cosineDistance(semantic_vector, {vec_literal}) AS distance
    FROM {CK_TABLE}
    WHERE crop_type = 'Tomato'
    ORDER BY distance ASC
    LIMIT {top_k}
    FORMAT JSON
    """

    resp = requests.post(
        CK_HTTP_URL,
        params={"user": CK_USER, "password": CK_PASSWORD},
        data=sql.encode("utf-8"),
        timeout=30,
    )
    resp.raise_for_status()
    return resp.json().get("data", [])


if __name__ == "__main__":
    # question = "西红柿现在长势如何？"
    # question = "西红柿现在结果了吗？" # question = "西红柿现在有没有病虫害？"
    # question = "西红柿现在的土壤情况怎么样？"
    question = "西红柿现在健康吗？"




    print(f"问题：{question}\n")

    records = query(question)
    for i, r in enumerate(records, 1):
        print(f"[{i}] 距离:{float(r['distance']):.4f}  温室:{r['greenhouse_id']}  {r['ts']}")
        print(f"     阶段:{r['growth_stage']}  健康:{r['health_score']}  病害:{r['disease_risk']}  问题:{r['issue_type']}")
        print(f"     {r['text_desc']}\n")
