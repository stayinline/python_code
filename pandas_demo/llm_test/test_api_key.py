"""
千问 API Key 可用性测试
测试项：
  1. Chat 对话（qwen-turbo）
  2. Embedding 向量化（text-embedding-v4）
  3. Rerank 重排序（gte-rerank-v2）
"""

from openai import OpenAI
from config import (
    MODEL_API_KEY, MODEL_BASE_URL, MODEL_TEMPERATURE,
    CHAT_MODEL_NAME, EMBEDDING_MODEL_NAME, RERANK_MODEL_NAME,
)

client = OpenAI(api_key=MODEL_API_KEY, base_url=MODEL_BASE_URL)


def test_chat():
    print("=" * 40)
    print("[1] Chat 测试")
    resp = client.chat.completions.create(
        model=CHAT_MODEL_NAME,
        temperature=MODEL_TEMPERATURE,
        messages=[{"role": "user", "content": "你好，请用一句话介绍你自己。"}],
    )
    print(f"  模型: {resp.model}")
    print(f"  回复: {resp.choices[0].message.content}")
    print(f"  tokens: prompt={resp.usage.prompt_tokens}, completion={resp.usage.completion_tokens}")
    print("  [OK]")


def test_embedding():
    print("=" * 40)
    print("[2] Embedding 测试")
    resp = client.embeddings.create(
        model=EMBEDDING_MODEL_NAME,
        input=["这是一段用于测试向量化的文本。"],
    )
    vec = resp.data[0].embedding
    print(f"  模型: {resp.model}")
    print(f"  向量维度: {len(vec)}")
    print(f"  前5维: {vec[:5]}")
    print("  [OK]")


def test_rerank():
    print("=" * 40)
    print("[3] Rerank 测试")
    # DashScope rerank 使用独立接口，通过 requests 调用
    import requests, json

    url = "https://dashscope.aliyuncs.com/api/v1/services/rerank/text-rerank/text-rerank"
    headers = {
        "Authorization": f"Bearer {MODEL_API_KEY}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": RERANK_MODEL_NAME,
        "input": {
            "query": "如何学习机器学习？",
            "documents": [
                "机器学习是人工智能的一个分支。",
                "今天天气很好，适合出门。",
                "深度学习需要大量数据和算力。",
            ],
        },
        "parameters": {"top_n": 3, "return_documents": False},
    }
    resp = requests.post(url, headers=headers, data=json.dumps(payload))
    resp.raise_for_status()
    result = resp.json()
    print(f"  模型: {result['output']['rerank_documents'][0].get('relevance_score', 'N/A')}")
    for item in result["output"]["rerank_documents"]:
        print(f"  index={item['index']}  score={item['relevance_score']:.4f}")
    print("  [OK]")


if __name__ == "__main__":
    results = {}
    for name, fn in [("chat", test_chat), ("embedding", test_embedding), ("rerank", test_rerank)]:
        try:
            fn()
            results[name] = "PASS"
        except Exception as e:
            print(f"  [FAIL] {e}")
            results[name] = f"FAIL: {e}"

    print("\n" + "=" * 40)
    print("测试汇总:")
    for k, v in results.items():
        status = "✓" if v == "PASS" else "✗"
        print(f"  {status} {k}: {v}")
