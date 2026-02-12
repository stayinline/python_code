import json
import time
import random
from kafka import KafkaProducer

# =====================
# Kafka 配置（与环境传感器一致）
# =====================
KAFKA_BROKERS = ["192.168.1.124:9092"]
TOPIC = "smart_agriculture_sensor_dirt"

producer = KafkaProducer(
    bootstrap_servers=KAFKA_BROKERS,
    value_serializer=lambda v: json.dumps(v).encode("utf-8")
)

# =====================
# 大棚 & 土壤传感器配置
# =====================
GREENHOUSE_ID = "gh_01"
SOIL_SENSOR_COUNT = 30

GREENHOUSE_SIZE = {
    "x": (0, 100),
    "y": (0, 30),
    "z": (0, 6)
}

# =====================
# 初始化土壤传感器
# =====================
soil_sensors = {}

for i in range(SOIL_SENSOR_COUNT):
    sensor_id = f"soil_sensor_{i:03d}"
    soil_sensors[sensor_id] = {
        "location": {
            "x": round(random.uniform(*GREENHOUSE_SIZE["x"]), 2),
            "y": round(random.uniform(*GREENHOUSE_SIZE["y"]), 2),
            "z": round(random.uniform(0.1, 0.3), 2)  # 埋地
        },
        "soil_temperature": random.uniform(15, 25),
        "soil_moisture": random.uniform(25, 55),
        "soil_ec": random.uniform(300, 1200),
        "soil_ph": random.uniform(5.8, 7.2),
        "soil_n": random.uniform(80, 200),
        "soil_p": random.uniform(20, 80),
        "soil_k": random.uniform(100, 300),
        "battery": random.randint(70, 100)
    }

# =====================
# 平滑波动函数
# =====================
def fluctuate(value, min_v, max_v, step):
    value += random.uniform(-step, step)
    return round(max(min_v, min(max_v, value)), 2)

# =====================
# 土壤传感器模拟函数（永不退出）
# =====================
def generate_dirt_data():
    print("🌱 Soil Sensor Simulator Started...")

    while True:
        loop_start = time.time()

        for sensor_id, s in soil_sensors.items():
            s["soil_temperature"] = fluctuate(s["soil_temperature"], 10, 30, 0.2)
            s["soil_moisture"] = fluctuate(s["soil_moisture"], 15, 80, 0.6)
            s["soil_ec"] = fluctuate(s["soil_ec"], 200, 2000, 40)
            s["soil_ph"] = fluctuate(s["soil_ph"], 5.5, 7.8, 0.05)
            s["soil_n"] = fluctuate(s["soil_n"], 50, 300, 5)
            s["soil_p"] = fluctuate(s["soil_p"], 10, 150, 3)
            s["soil_k"] = fluctuate(s["soil_k"], 50, 400, 6)

            # 电量缓慢下降
            s["battery"] = max(20, s["battery"] - random.choice([0, 0, 1]))

            data = {
                "sensor_id": sensor_id,
                "sensor_type": "SOIL",
                "greenhouse_id": GREENHOUSE_ID,
                "timestamp": int(time.time() * 1000),
                "location": s["location"],
                "metrics": {
                    "soil_temperature": s["soil_temperature"],
                    "soil_moisture": s["soil_moisture"],
                    "soil_ec": s["soil_ec"],
                    "soil_ph": s["soil_ph"],
                    "soil_n": s["soil_n"],
                    "soil_p": s["soil_p"],
                    "soil_k": s["soil_k"]
                },
                "device": {
                    "battery": s["battery"],
                    "status": "ONLINE" if s["battery"] > 25 else "WARN",
                    "firmware": "v1.0.0"
                }
            }

            producer.send(TOPIC, data)
            print(data)

        producer.flush()

        # 保证「每个传感器 3 秒 1 条」
        elapsed = time.time() - loop_start
        time.sleep(max(0, 3 - elapsed))


if __name__ == "__main__":
    generate_dirt_data()