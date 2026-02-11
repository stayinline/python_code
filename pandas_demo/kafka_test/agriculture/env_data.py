import json
import time
import random
from kafka import KafkaProducer

# =====================
# Kafka 配置
# =====================
KAFKA_BROKERS = ["192.168.1.124:9092"]
TOPIC = "smart_agriculture_sensor"

producer = KafkaProducer(
    bootstrap_servers=KAFKA_BROKERS,
    value_serializer=lambda v: json.dumps(v).encode("utf-8")
)

# =====================
# 大棚 & 传感器配置
# =====================
GREENHOUSE_ID = "gh_01"
SENSOR_COUNT = 20

GREENHOUSE_SIZE = {
    "x": (0, 100),
    "y": (0, 30),
    "z": (0, 6)
}

# =====================
# 初始化传感器（固定位置 + 初始值）
# =====================
sensors = {}

for i in range(SENSOR_COUNT):
    sensor_id = f"sensor_{i:03d}"
    sensors[sensor_id] = {
        "location": {
            "x": round(random.uniform(*GREENHOUSE_SIZE["x"]), 2),
            "y": round(random.uniform(*GREENHOUSE_SIZE["y"]), 2),
            "z": round(random.uniform(0.5, 2.5), 2)
        },
        "temperature": random.uniform(20, 28),
        "humidity": random.uniform(50, 80),
        "co2": random.uniform(400, 1200),
        "light": random.uniform(1000, 60000),
        "soil_temperature": random.uniform(15, 25),
        "soil_moisture": random.uniform(30, 60),
        "battery": random.randint(60, 100)
    }


# =====================
# 数值平滑波动函数
# =====================
def fluctuate(value, min_v, max_v, step):
    value += random.uniform(-step, step)
    return round(max(min_v, min(max_v, value)), 2)


def generate_env_data():
    global sensor_id
    while True:
        for sensor_id, s in sensors.items():
            # 平滑变化
            s["temperature"] = fluctuate(s["temperature"], 15, 35, 0.3)
            s["humidity"] = fluctuate(s["humidity"], 35, 95, 1.0)
            s["co2"] = fluctuate(s["co2"], 350, 2000, 30)
            s["light"] = fluctuate(s["light"], 0, 120000, 2000)
            s["soil_temperature"] = fluctuate(s["soil_temperature"], 10, 30, 0.2)
            s["soil_moisture"] = fluctuate(s["soil_moisture"], 20, 80, 0.8)

            # 电量缓慢下降
            s["battery"] = max(20, s["battery"] - random.choice([0, 0, 0, 1]))

            data = {
                "sensor_id": sensor_id,
                "greenhouse_id": GREENHOUSE_ID,
                "timestamp": int(time.time() * 1000),
                "location": s["location"],
                "metrics": {
                    "temperature": s["temperature"],
                    "humidity": s["humidity"],
                    "co2": int(s["co2"]),
                    "light": int(s["light"]),
                    "soil_temperature": s["soil_temperature"],
                    "soil_moisture": s["soil_moisture"]
                },
                "device": {
                    "battery": s["battery"],
                    "status": "ONLINE" if s["battery"] > 25 else "WARN",
                    "firmware": "v1.2.3"
                }
            }

            producer.send(TOPIC, data)
            print(data)

        producer.flush()
        time.sleep(1)  # 每个传感器 ≥ 1 条 / 秒
