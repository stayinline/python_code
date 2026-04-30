import unittest
from openai import OpenAI
from llm_test.config import MODEL_API_KEY, MODEL_BASE_URL, CHAT_MODEL_NAME


class TestQwenAPIKey(unittest.TestCase):
    """测试千问API KEY的可用性"""

    def test_api_key_availability(self):
        """测试API KEY是否可以正常访问千问模型"""
        # 初始化OpenAI客户端（兼容千问API）
        client = OpenAI(
            api_key=MODEL_API_KEY,
            base_url=MODEL_BASE_URL
        )

        # 发送一个简单的测试请求
        try:
            response = client.chat.completions.create(
                model=CHAT_MODEL_NAME,
                messages=[
                    {"role": "system", "content": "你是一个助手。"},
                    {"role": "user", "content": "你好，请回复你是什么版本的大模型，然后追加'API KEY验证成功'"}
                ],
                temperature=0.01,
                max_tokens=50
            )
            
            # 检查响应
            self.assertIsNotNone(response)
            self.assertTrue(len(response.choices) > 0)
            content = response.choices[0].message.content
            print(f"API响应: {content}")
            self.assertIn("API KEY验证成功", content)
            print("✅ API KEY验证成功！")
            
        except Exception as e:
            self.fail(f"API KEY验证失败: {str(e)}")


if __name__ == "__main__":
    unittest.main()