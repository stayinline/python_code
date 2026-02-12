import json
import time
import random
import uuid
from kafka import KafkaProducer

# =====================
# Kafka 配置
# =====================
KAFKA_BROKERS = ["192.168.1.124:9092"]
TOPIC = "smart_agriculture_plant_vision"

producer = KafkaProducer(
    bootstrap_servers=KAFKA_BROKERS,
    value_serializer=lambda v: json.dumps(v).encode("utf-8")
)

# =====================
# 大棚 & 摄像头配置
# =====================
GREENHOUSE_ID = "gh_01"
CAMERA_COUNT = 6

CAMERAS = {}

for i in range(CAMERA_COUNT):
    camera_id = f"cam_{i:02d}"
    CAMERAS[camera_id] = {
        "plant_height": random.uniform(50, 70),
        "leaf_count": random.randint(18, 26),
        "canopy": random.uniform(0.6, 0.75),
        "chlorophyll": random.uniform(38, 44),
        "fruit_count": random.randint(6, 14),
    }

# =====================
# 平滑波动函数（和你一致）
# =====================
def fluctuate(value, min_v, max_v, step):
    value += random.uniform(-step, step)
    return round(max(min_v, min(max_v, value)), 2)

# =====================
# 植株图片识别模拟（永不退出）
# =====================
def generate_plant_vision_data():
    print("📷 Plant Vision AI Simulator Started...")

    while True:
        loop_start = time.time()

        for camera_id, c in CAMERAS.items():
            # ===== 平滑变化 =====
            c["plant_height"] = fluctuate(c["plant_height"], 40, 120, 0.3)
            c["leaf_count"] = int(fluctuate(c["leaf_count"], 10, 40, 1))
            c["canopy"] = fluctuate(c["canopy"], 0.3, 0.95, 0.02)
            c["chlorophyll"] = fluctuate(c["chlorophyll"], 30, 50, 0.4)
            c["fruit_count"] = int(fluctuate(c["fruit_count"], 0, 30, 1))

            # ===== 生长阶段推断 =====
            if c["plant_height"] < 45:
                growth_stage = "SEEDLING"
            elif c["fruit_count"] > 5:
                growth_stage = "FRUITING"
            else:
                growth_stage = "FLOWERING"

            # ===== 胁迫判断 =====
            water_stress = "HIGH" if c["canopy"] < 0.45 else "NORMAL"
            nutrient_stress = "N_DEFICIENCY" if c["chlorophyll"] < 35 else "NONE"

            data = {
                "plant_detect_id": f"plant_det_{uuid.uuid4().hex[:12]}",
                "greenhouse_id": GREENHOUSE_ID,
                "camera_id": camera_id,
                "timestamp": int(time.time() * 1000),

                "plant_basic": {
                    "crop_type": "Tomato",
                    "growth_stage": growth_stage,
                    "plant_height_cm": round(c["plant_height"], 1),
                    "leaf_count": c["leaf_count"],
                    "canopy_coverage": round(c["canopy"], 2)
                },

                "plant_health": {
                    "leaf_color_index": round(random.uniform(0.75, 0.9), 2),
                    "chlorophyll_index": round(c["chlorophyll"], 1),
                    "wilting_score": round(random.uniform(0.02, 0.12), 2),
                    "disease_risk": "LOW",
                    "pest_risk": random.choice(["LOW", "MEDIUM"])
                },

                "fruit_info": {
                    "fruit_count": c["fruit_count"],
                    "avg_fruit_diameter_mm": round(random.uniform(25, 38), 1),
                    "fruit_color_stage": "GREEN"
                },

                "stress_analysis": {
                    "water_stress": water_stress,
                    "nutrient_stress": nutrient_stress,
                    "light_stress": "NONE"
                },

                "confidence": round(random.uniform(0.90, 0.97), 2),
                "model_version": "plant-vision-v2.1"
            }

            producer.send(TOPIC, data)
            print(data)

        producer.flush()

        # 每个摄像头 5 秒 1 次识别
        elapsed = time.time() - loop_start
        time.sleep(max(0, 5 - elapsed))


if __name__ == "__main__":
    generate_plant_vision_data()
