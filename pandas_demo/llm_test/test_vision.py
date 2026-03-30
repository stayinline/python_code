"""
千问视觉模型 Demo
模型: Qwen2.5-VL-7B-Instruct
接口: http://124.221.45.104:9304/v1/chat/completions
"""

import base64
import requests
from pathlib import Path

VL_BASE_URL = "http://124.221.45.104:9304/v1"
VL_MODEL = "Qwen2.5-VL-7B-Instruct"


def encode_image_to_base64(image_path: str) -> str:
    """将本地图片编码为 base64"""
    with open(image_path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")


def get_image_media_type(image_path: str) -> str:
    suffix = Path(image_path).suffix.lower()
    return {
        ".jpg": "image/jpeg",
        ".jpeg": "image/jpeg",
        ".png": "image/png",
        ".gif": "image/gif",
        ".webp": "image/webp",
    }.get(suffix, "image/jpeg")


def chat_with_image(image_source: str, prompt: str, use_url: bool = False) -> str:
    """
    发送图片 + 文本给视觉模型

    :param image_source: 本地图片路径 或 图片URL
    :param prompt:       提问内容
    :param use_url:      True 表示 image_source 是网络URL，False 表示本地路径
    :return:             模型回复文本
    """
    if use_url:
        image_content = {
            "type": "image_url",
            "image_url": {"url": image_source},
        }
    else:
        b64 = encode_image_to_base64(image_source)
        media_type = get_image_media_type(image_source)
        image_content = {
            "type": "image_url",
            "image_url": {"url": f"data:{media_type};base64,{b64}"},
        }

    payload = {
        "model": VL_MODEL,
        "messages": [
            {
                "role": "user",
                "content": [
                    image_content,
                    {"type": "text", "text": prompt},
                ],
            }
        ],
        "max_tokens": 1024,
        "temperature": 0.01,
    }

    resp = requests.post(
        f"{VL_BASE_URL}/chat/completions",
        json=payload,
        timeout=60,
    )
    resp.raise_for_status()
    return resp.json()["choices"][0]["message"]["content"]


# ──────────────────────────────────────────────
# 使用示例：把下面的路径/URL换成你自己的图片
# ──────────────────────────────────────────────
if __name__ == "__main__":
    # ① 本地图片
    LOCAL_IMAGE = "D:\code\python\pandas_demo\llm_test\PDF测试图片.png"   # <-- 改成你的图片路径
    LOCAL_PROMPT = "请描述这张图片的内容"

    # # ② 网络图片URL（可选）
    # REMOTE_IMAGE = "https://example.com/sample.jpg"   # <-- 改成你的图片URL
    # REMOTE_PROMPT = "图中有哪些文字？"

    print("=" * 50)
    print(f"模型: {VL_MODEL}")
    print(f"接口: {VL_BASE_URL}")
    print("=" * 50)

    # 测试本地图片
    if Path(LOCAL_IMAGE).exists():
        print(f"\n[本地图片] {LOCAL_IMAGE}")
        print(f"问题: {LOCAL_PROMPT}")
        answer = chat_with_image(LOCAL_IMAGE, LOCAL_PROMPT, use_url=False)
        print(f"回答: {answer}")
    else:
        print(f"\n[跳过] 本地图片不存在: {LOCAL_IMAGE}")

    # 如需测试网络图片，取消下面注释
    # print(f"\n[网络图片] {REMOTE_IMAGE}")
    # print(f"问题: {REMOTE_PROMPT}")
    # answer = chat_with_image(REMOTE_IMAGE, REMOTE_PROMPT, use_url=True)
    # print(f"回答: {answer}")
