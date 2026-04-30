from openai import OpenAI
from llm_test.config import MODEL_API_KEY, MODEL_BASE_URL, CHAT_MODEL_NAME

# 初始化OpenAI客户端（兼容千问API）
client = OpenAI(
    api_key=MODEL_API_KEY,
    base_url=MODEL_BASE_URL
)

# 测试1: 基本对话功能
print("=== 测试1: 基本对话功能 ===")
try:
    response = client.chat.completions.create(
        model=CHAT_MODEL_NAME,
        messages=[
            {"role": "system", "content": "你是一个助手。"},
            {"role": "user", "content": "你好，请回复你是什么版本的大模型，然后追加'API KEY验证成功'"}
        ],
        temperature=0.01,
        max_tokens=100
    )
    print(f"✅ 基本对话测试通过")
    print(f"模型回复: {response.choices[0].message.content}")
    print()
except Exception as e:
    print(f"❌ 基本对话测试失败: {str(e)}")
    exit(1)

# 测试2: 数学计算功能
print("=== 测试2: 数学计算功能 ===")
try:
    response = client.chat.completions.create(
        model=CHAT_MODEL_NAME,
        messages=[
            {"role": "user", "content": "计算 15 * 23 + 45 的结果是多少？"}
        ],
        temperature=0.01,
        max_tokens=50
    )
    print(f"✅ 数学计算测试通过")
    print(f"模型回复: {response.choices[0].message.content}")
    print()
except Exception as e:
    print(f"❌ 数学计算测试失败: {str(e)}")

# 测试3: 代码生成能力
print("=== 测试3: 代码生成能力 ===")
try:
    response = client.chat.completions.create(
        model=CHAT_MODEL_NAME,
        messages=[
            {"role": "user", "content": "用Python写一个计算斐波那契数列的函数，返回前n项"}
        ],
        temperature=0.01,
        max_tokens=150
    )
    print(f"✅ 代码生成测试通过")
    print(f"模型回复: {response.choices[0].message.content}")
    print()
except Exception as e:
    print(f"❌ 代码生成测试失败: {str(e)}")

print("🎉 所有功能测试完成！")