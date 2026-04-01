"""
图片向量搜索 Demo
- 存入 5 张示例图片（CLIP 向量化）
- 按图搜图（near_vector 语义搜索）

依赖: pip install sentence-transformers pillow weaviate-client
"""

import os
import base64
import weaviate
from weaviate.connect import ConnectionParams
from weaviate.collections.classes.config import Configure
from weaviate.classes.config import DataType, Property
from weaviate.classes.query import MetadataQuery
from PIL import Image, ImageDraw, ImageFont
from sentence_transformers import SentenceTransformer

# ─── 配置 ───────────────────────────────────────────────
WEAVIATE_URL   = "http://192.168.1.131:18080"
GRPC_PORT      = 50051
COLLECTION     = "ImageSearch"
IMAGE_DIR      = os.path.join(os.path.dirname(__file__), "sample_images")
RESULT_DIR     = os.path.join(os.path.dirname(__file__), "search_results")
HF_CACHE_DIR   = os.path.join(os.path.dirname(__file__), "huggingface_cache")

# ─── 1. 生成 5 张示例图片 ────────────────────────────────
def create_sample_images() -> list[dict]:
    os.makedirs(IMAGE_DIR, exist_ok=True)

    specs = [
        {
            "name":  "red_apple.png",
            "label": "红苹果",
            "bg":    (240, 240, 240),
            "shape": "circle",
            "color": (200, 40, 40),
        },
        {
            "name":  "blue_sky.png",
            "label": "蓝天",
            "bg":    (135, 206, 235),
            "shape": "rect",
            "color": (50, 120, 220),
        },
        {
            "name":  "green_tree.png",
            "label": "绿树",
            "bg":    (220, 240, 220),
            "shape": "triangle",
            "color": (34, 139, 34),
        },
        {
            "name":  "yellow_sun.png",
            "label": "黄色太阳",
            "bg":    (255, 250, 200),
            "shape": "star",
            "color": (255, 200, 0),
        },
        {
            "name":  "purple_flower.png",
            "label": "紫色花朵",
            "bg":    (240, 230, 255),
            "shape": "oval",
            "color": (148, 0, 211),
        },
    ]

    result = []
    for s in specs:
        path = os.path.join(IMAGE_DIR, s["name"])
        img  = Image.new("RGB", (256, 256), color=s["bg"])
        draw = ImageDraw.Draw(img)

        if s["shape"] == "circle":
            draw.ellipse([48, 48, 208, 208], fill=s["color"])
        elif s["shape"] == "rect":
            draw.rectangle([40, 80, 216, 200], fill=s["color"])
            # 画几朵云
            draw.ellipse([20, 30, 100, 80],  fill=(255, 255, 255))
            draw.ellipse([60, 20, 160, 70],  fill=(255, 255, 255))
            draw.ellipse([120, 35, 200, 80], fill=(255, 255, 255))
        elif s["shape"] == "triangle":
            draw.polygon([(128, 30), (30, 220), (226, 220)], fill=s["color"])
            # 树干
            draw.rectangle([110, 210, 146, 240], fill=(101, 67, 33))
        elif s["shape"] == "star":
            # 简单五角星近似
            pts = []
            import math
            cx, cy, r1, r2 = 128, 128, 100, 45
            for i in range(10):
                angle = math.pi / 2 + i * math.pi / 5
                r = r1 if i % 2 == 0 else r2
                pts.append((cx + r * math.cos(angle), cy - r * math.sin(angle)))
            draw.polygon(pts, fill=s["color"])
        elif s["shape"] == "oval":
            draw.ellipse([40, 70, 216, 186], fill=s["color"])
            # 花瓣效果
            for angle_deg in range(0, 360, 45):
                import math
                a = math.radians(angle_deg)
                ex = 128 + 80 * math.cos(a)
                ey = 128 + 80 * math.sin(a)
                draw.ellipse([ex - 25, ey - 25, ex + 25, ey + 25], fill=s["color"])
            draw.ellipse([88, 88, 168, 168], fill=(255, 220, 0))

        # 标签文字
        draw.rectangle([0, 226, 256, 256], fill=(0, 0, 0, 180))
        draw.text((8, 232), s["label"], fill=(255, 255, 255))

        img.save(path)
        result.append({"path": path, "name": s["name"], "label": s["label"]})
        print(f"  生成: {s['label']} -> {path}")

    return result


# ─── 2. 图片编解码工具 ───────────────────────────────────
def encode_image_to_vector(model: SentenceTransformer, path: str) -> list[float]:
    img = Image.open(path).convert("RGB")
    return model.encode(img).tolist()


def image_to_b64(path: str) -> str:
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")


def b64_to_image(b64: str, save_path: str):
    data = base64.b64decode(b64)
    with open(save_path, "wb") as f:
        f.write(data)


# ─── 3. 保存搜索结果为拼图 ──────────────────────────────
def save_result_grid(query_path: str, result_items: list[dict], save_path: str):
    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    thumb_size = (200, 200)
    padding    = 10
    cols       = 1 + len(result_items)
    width      = cols * (thumb_size[0] + padding) + padding
    height     = thumb_size[1] + padding * 2 + 40

    grid = Image.new("RGB", (width, height), (50, 50, 50))
    draw = ImageDraw.Draw(grid)

    # 查询图
    q_img = Image.open(query_path).resize(thumb_size)
    grid.paste(q_img, (padding, padding))
    draw.text((padding, thumb_size[1] + padding + 5), "【查询图】", fill=(255, 255, 0))

    # 分隔线
    x_sep = padding + thumb_size[0] + padding // 2
    draw.line([(x_sep, 0), (x_sep, height)], fill=(200, 200, 200), width=2)

    # 结果图
    for i, item in enumerate(result_items):
        x = (i + 1) * (thumb_size[0] + padding) + padding
        # 从 base64 恢复图片
        tmp_path = os.path.join(RESULT_DIR, f"_tmp_{i}.png")
        b64_to_image(item["image_base64"], tmp_path)
        r_img = Image.open(tmp_path).resize(thumb_size)
        grid.paste(r_img, (x, padding))
        caption = f"#{i+1} {item['label']} d={item['distance']:.3f}"
        draw.text((x, thumb_size[1] + padding + 5), caption, fill=(255, 255, 255))

    grid.save(save_path)
    print(f"  搜索结果图已保存: {save_path}")


# ─── 主流程 ─────────────────────────────────────────────
def main():
    # 1. 生成示例图片
    print("=" * 50)
    print("1. 生成示例图片")
    print("=" * 50)
    images = create_sample_images()

    # 2. 加载 CLIP 模型
    print("\n" + "=" * 50)
    print("2. 加载 CLIP 模型 (clip-ViT-B-32)")
    print("=" * 50)
    model = SentenceTransformer(
        "clip-ViT-B-32",
        cache_folder=HF_CACHE_DIR,
    )
    print("  模型加载完成 ✅")

    # 3. 连接 Weaviate
    print("\n" + "=" * 50)
    print("3. 连接 Weaviate")
    print("=" * 50)
    client = weaviate.WeaviateClient(
        connection_params=ConnectionParams.from_url(WEAVIATE_URL, grpc_port=GRPC_PORT)
    )
    client.connect()

    if not client.is_ready():
        raise RuntimeError("Weaviate 未就绪，请检查服务")
    print(f"  连接成功: {WEAVIATE_URL} ✅")

    try:
        # 4. 初始化 Collection
        print("\n" + "=" * 50)
        print("4. 初始化集合")
        print("=" * 50)
        if client.collections.exists(COLLECTION):
            client.collections.delete(COLLECTION)
            print(f"  已删除旧集合: {COLLECTION}")

        client.collections.create(
            name=COLLECTION,
            properties=[
                Property(name="filename",     data_type=DataType.TEXT),
                Property(name="label",        data_type=DataType.TEXT),
                Property(name="image_base64", data_type=DataType.TEXT),  # base64 存储
            ],
            vectorizer_config=Configure.Vectorizer.none(),
        )
        print(f"  集合已创建: {COLLECTION}")

        # 5. 存入 5 张图片
        print("\n" + "=" * 50)
        print("5. 存入 5 张图片")
        print("=" * 50)
        collection = client.collections.get(COLLECTION)

        for img in images:
            vector = encode_image_to_vector(model, img["path"])
            b64    = image_to_b64(img["path"])

            collection.data.insert(
                properties={
                    "filename":     img["name"],
                    "label":        img["label"],
                    "image_base64": b64,
                },
                vector=vector,
            )
            print(f"  存入: {img['label']}  向量维度={len(vector)}")

        # 验证存储数量
        stats = collection.aggregate.over_all(total_count=True)
        print(f"\n  共存入图片: {stats.total_count} 张 ✅")

        # 6. 按图搜图
        print("\n" + "=" * 50)
        print("6. 按图搜图")
        print("=" * 50)

        # 依次用每张图做查询，展示 Top-3
        for query_img in images:
            print(f"\n  查询图: [{query_img['label']}]")
            q_vector = encode_image_to_vector(model, query_img["path"])

            results = collection.query.near_vector(
                near_vector=q_vector,
                limit=3,
                return_metadata=MetadataQuery(distance=True),
            )

            result_items = []
            for rank, obj in enumerate(results.objects):
                label    = obj.properties["label"]
                distance = obj.metadata.distance
                marker   = "← (自身)" if label == query_img["label"] else ""
                print(f"    Top{rank+1}: {label}  distance={distance:.4f} {marker}")
                result_items.append({
                    "label":        label,
                    "image_base64": obj.properties["image_base64"],
                    "distance":     distance,
                })

            # 保存结果拼图
            safe_name  = query_img["name"].replace(".png", "")
            result_img = os.path.join(RESULT_DIR, f"result_{safe_name}.png")
            save_result_grid(query_img["path"], result_items, result_img)

    finally:
        client.close()
        print("\n连接已关闭")

    print("\n" + "=" * 50)
    print("Demo 完成 ✅")
    print(f"示例图片: {IMAGE_DIR}")
    print(f"搜索结果: {RESULT_DIR}")
    print("=" * 50)


if __name__ == "__main__":
    main()
