"""千问图片生成测试脚本

使用 HTTP 请求调用 DashScope 多模态生成 API 生成图片。
对应 curl: https://dashscope.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation
安装依赖：pip install requests
"""

import time
from pathlib import Path
import requests

# ====== 可配置项 ======
# 图像生成模型，如 wan2.7-image-pro / wan2.6-image / qwen-image-2.0-pro 等
IMAGE_MODEL = "qwen-image-2.0-pro"
# PROMPT = "一只可爱的猫咪坐在窗台上晒太阳，温暖的光线透过玻璃洒在猫身上"
PROMPT=f"""核心风格参考
《魔道祖师》动画美术风格，水墨国风仙侠，飘逸写意与精致细节结合，高对比度光影，电影级分镜，动态张力拉满，古风武侠质感，色彩淡雅高级，大量云雾水墨特效，人物身形修长俊美，衣袂翻飞飘逸，眼神锐利有故事感。
完整剧情提示词
【主场景】 暴雨倾盆的江南断桥之上，青石板路被雨水冲刷得油亮反光，桥下是湍急的黑色河水，远处是朦胧的水墨青山和竹林，闪电划破夜空照亮整个场景，雨水在空气中形成密集的雨帘。
【女主角・凌霜月】 20 岁左右，名门正派青云宗首席女弟子，清冷绝艳，银灰色长发高束成马尾，几缕碎发被雨水打湿贴在脸颊，剑眉星目，眼神冰冷如霜，嘴角带着一丝倔强的血迹。身穿月白色绣银线流云纹劲装，外披半透明的白色纱衣，衣摆和袖口被雨水浸透，右手紧握一柄泛着寒光的冰魄长剑，剑尖指向地面，剑身凝结着细碎的冰晶。她身体微微前倾，左腿在前弓步，右腿在后蹬地，全身肌肉紧绷，正准备发动致命一击，周身环绕着淡蓝色的冰系剑气，将周围的雨水冻结成冰粒。
【男主角・墨尘渊】 22 岁左右，亦正亦邪的孤影阁少主，俊美邪魅，墨黑色长发随意披散，额前有一缕红发挑染，狭长的丹凤眼，眼神深邃复杂，带着一丝嘲讽和痛苦。身穿玄黑色绣暗金色龙纹长袍，领口和袖口绣着血色彼岸花，黑色披风在狂风中猎猎作响，左手持一柄通体漆黑的噬魂古剑，剑身缠绕着黑色的魔气。他侧身站立，右手背在身后，看似漫不经心，实则全身戒备，周身环绕着黑色的水墨状魔气，将靠近的雨水蒸发成白雾。
【对决瞬间】 两人相距三丈，剑气与魔气在空中激烈碰撞，形成一道巨大的能量冲击波，将桥面上的雨水向四周炸开，形成一个圆形的无水区域。闪电再次照亮两人的脸庞，女主角眼中是滔天的恨意，男主角眼中是难以言说的悲伤。背景中隐约可见断桥断裂的栏杆和飘落的竹叶，整个画面充满了宿命对决的悲壮感和张力。
【技术参数】 8K 超高清，极致细节，电影级光影，体积光，全局光照，景深效果，动态模糊，水墨渲染，赛璐璐风格，线条流畅清晰，色彩层次丰富，氛围渲染到位，分镜构图具有冲击力，人物比例协调，动作自然流畅。"""
# API_KEY = "sk-sp-djI.oTn5D4s8gardX9UeCas0OPrTNAofawZbWHGMPzHhlXXR5x1J53HD80utDyaOxI8XiMkEpYoAxtS4OVihG0wpb0Gk4ViBBSDvp3P-9qXTwRKaooimi0T6QWSkVtP_xTtR5kaUA8BliYNLkZuvPxO3GgAmHrEvRcFp7SItvt1wZ0sCTFWjhWg9SCMCe86MU_9e.MEUCIQDnRAcMIgq23T1Rb3z6AR9RksnYdcRHI33X7Rl8PfOLNgIgWu9o3Ln3ifOn0yoAhJBDoN-7tKnC1idAPEIhCJuZtKM"
API_KEY = "sk-2a0c4ae6def84744956ac778b9408dbc"
OUTPUT_DIR = Path(__file__).parent / "generated_images"
API_URL = "https://dashscope.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation"

# 请求参数（对应 curl 的 parameters 部分）
# qwen-image-2.0-pro 参数，size 可选：1024*1024 / 2048*2048 等（512~2048 范围内）
PARAMETERS = {
    "size": "2048*2048",    # 尺寸，如 1024*1024 / 2048*2048
    "n": 1,                  # 生成图片数量
    "watermark": False,      # 是否添加水印
    "prompt_extend": True,   # 开启提示词智能改写
    # "negative_prompt": "低分辨率，低画质，肢体畸形",  # 反向提示词（可选）
}
# ======================


def generate_image(model: str, prompt: str, api_key: str, output_dir: Path,
                   parameters: dict = None) -> list[str]:
    """调用 DashScope 多模态生成 API 生成图片，返回保存的文件路径列表"""
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}",
    }

    payload = {
        "model": model,
        "input": {
            "messages": [
                {
                    "role": "user",
                    "content": [{"text": prompt}]
                }
            ]
        },
        "parameters": parameters or {},
    }

    print(f"正在调用模型 {model} 生成图片...")
    print(f"Prompt: {prompt}")

    resp = requests.post(API_URL, headers=headers, json=payload)
    resp.raise_for_status()

    result = resp.json()
    print(f"API 响应: {result}")

    if "output" not in result:
        print(f"调用失败！响应: {result}")
        return []

    output_dir.mkdir(parents=True, exist_ok=True)
    paths = []

    # 解析返回的图片 URL
    # 响应格式: {"output": {"choices": [{"message": {"content": [{"image": "..."}, ...]}}]}}
    choices = result["output"].get("choices", [])
    if not choices:
        print("未找到图片数据")
        return []

    content_items = choices[0].get("message", {}).get("content", [])
    for i, item in enumerate(content_items):
        if "image" in item:
            url = item["image"]
            file_path = output_dir / f"image_{int(time.time())}_{i}.png"
            img_resp = requests.get(url)
            with open(file_path, "wb") as f:
                f.write(img_resp.content)
            paths.append(str(file_path))
            print(f"图片已保存: {file_path}")

    return paths


if __name__ == "__main__":
    generate_image(
        model=IMAGE_MODEL,
        prompt=PROMPT,
        api_key=API_KEY,
        output_dir=OUTPUT_DIR,
        parameters=PARAMETERS,
    )
