from kafka import KafkaProducer, KafkaConsumer
import json
from datetime import datetime
import time

# Kafka配置
KAFKA_BROKER = '192.168.1.124:9092'
# KAFKA_BROKER = '192.168.250.42:9092'
TOPIC_NAME = 'test_ck'


def create_message(id: int, message: str, value: float) -> dict:
    """创建符合格式的消息"""
    return {
        "id": id,
        "message": message,
        "value": value,
        "event_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }


def kafka_producer():
    """Kafka消息生产者"""
    try:
        # 创建生产者实例
        producer = KafkaProducer(
            bootstrap_servers=KAFKA_BROKER,
            value_serializer=lambda v: json.dumps(v).encode('utf-8')  # 序列化消息为JSON
        )

        # 生成一条测试消息
        message = create_message(
            id=13,
            message="贺茂岭测试系统监控数据",
            value=80.3
        )

        # 发送消息到指定topic
        producer.send(TOPIC_NAME, value=message)
        producer.flush()  # 确保消息被发送
        print(f"成功发送消息: {message}")

    except Exception as e:
        print(f"生产者错误: {str(e)}")
    finally:
        if 'producer' in locals():
            producer.close()


def kafka_consumer():
    """Kafka消息消费者"""
    try:
        # 创建消费者实例
        consumer = KafkaConsumer(
            TOPIC_NAME,
            bootstrap_servers=KAFKA_BROKER,
            auto_offset_reset='earliest',  # 从最早的消息开始消费
            value_deserializer=lambda m: json.loads(m.decode('utf-8')),  # 反序列化JSON消息
            group_id='test_ck_group'  # 消费者组ID
        )

        print("开始消费消息，按Ctrl+C停止...")
        # 消费消息
        for message in consumer:
            print(f"\n收到消息:")
            print(f"分区: {message.partition}")
            print(f"偏移量: {message.offset}")
            print(f"内容: {message.value}")

    except KeyboardInterrupt:
        print("\n用户中断消费")
    except Exception as e:
        print(f"消费者错误: {str(e)}")
    finally:
        if 'consumer' in locals():
            consumer.close()


if __name__ == "__main__":
    # 先生产一条消息
    print("=== 开始生产消息 ===")
    kafka_producer()

    # # 等待片刻，确保消息已被Kafka处理
    # time.sleep(2)
    #
    # # 再消费消息
    # print("\n=== 开始消费消息 ===")
    # kafka_consumer()
