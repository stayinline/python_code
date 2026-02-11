import json
import time
import random
from kafka import KafkaProducer

# =====================
# Kafka 配置（完全一致）
# =====================
KAFKA_BROKERS = ["192.168.1.124:9092"]
TOPIC = "smart_agriculture_sensor_persion"

producer = KafkaProducer(
    bootstrap_servers=KAFKA_BROKERS,
    value_serializer=lambda v: json.dumps(v).encode("utf-8")
)

GREENHOUSE_ID = "gh_01"

OPERATORS = [
    {"id": "op_001", "name": "Li Ming", "role": "Agronomist"},
    {"id": "op_002", "name": "Zhang Wei", "role": "Field Operator"},
    {"id": "op_003", "name": "AI_ASSIST", "role": "AI System"}
]

OPERATION_TYPES = [
    "IRRIGATION",
    "FERTILIZATION",
    "VENTILATION",
    "SHADE_CONTROL",
    "PEST_CONTROL",
    "INSPECTION"
]

ZONES = ["ZONE_A", "ZONE_B", "ZONE_C"]


def generate_manual_operation():
    operator = random.choice(OPERATORS)
    op_type = random.choice(OPERATION_TYPES)

    data = {
        "operation_id": f"op_{int(time.time() * 1000)}",
        "data_type": "MANUAL_OPERATION",
        "greenhouse_id": GREENHOUSE_ID,
        "timestamp": int(time.time() * 1000),

        "operator": operator,

        "operation": {
            "operation_type": op_type,
            "target_zone": random.choice(ZONES),
            "duration_sec": random.randint(300, 1800)
        },

        "control_params": {
            "irrigation_mode": random.choice(["DRIP", "SPRINKLER", None]),
            "water_volume_l": round(random.uniform(50, 300), 1) if op_type == "IRRIGATION" else None,
            "fertilizer_type": random.choice(["NPK", "UREA", "ORGANIC", None]),
            "fertilizer_amount_kg": round(random.uniform(1, 8), 2) if op_type == "FERTILIZATION" else None
        },

        "decision": {
            "trigger_source": random.choice(["MANUAL", "AI", "RULE"]),
            "reason": random.choice([
                "Low soil moisture",
                "AI recommendation",
                "Routine operation",
                "Crop growth stage requirement",
                "Abnormal sensor alert"
            ]),
            "expected_effect": random.choice([
                "Increase soil moisture",
                "Improve nutrient supply",
                "Reduce heat stress",
                "Prevent pest outbreak"
            ]),
            "related_sensor_snapshot": {
                "soil_moisture": round(random.uniform(20, 60), 1),
                "soil_ec": round(random.uniform(400, 1200), 1),
                "soil_temperature": round(random.uniform(15, 28), 1)
            }
        },

        "result": {
            "execution_status": random.choice(["SUCCESS", "SUCCESS", "SUCCESS", "FAIL"]),
            "audit_required": random.choice([False, False, True]),
            "remark": ""
        }
    }

    return data


# =====================
# 主循环：每分钟 1 条
# =====================
def generate_persion_data():
    print("👨‍🌾 Manual Farming Operation Simulator Started...")

    while True:
        record = generate_manual_operation()
        producer.send(TOPIC, record)
        producer.flush()
        print(record)

        time.sleep(10)

if __name__ == "__main__":
    generate_persion_data()