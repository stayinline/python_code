from kafka import KafkaProducer, KafkaConsumer
import json
from datetime import datetime
import time
import random
from threading import Event

# Kafka配置
KAFKA_BROKER = '192.168.1.124:9092'
# KAFKA_BROKER = '192.168.250.42:9092'
TOPIC_NAME = 'test_ck'
MESSAGES_PER_SECOND = 500  # 每秒发送的消息数量
RUN_DURATION = 0  # 运行时长(秒)，0表示无限运行


def create_message(id: int) -> dict:
    """创建符合格式的消息，每条消息内容略有不同"""
    return {
        "id": id,
        "message": f"系统监控数据 #{id}",
        "value": round(random.uniform(50.0, 100.0), 2),  # 随机数值
        "event_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]  # 精确到毫秒
    }


def kafka_high_speed_producer():
    """高速Kafka消息生产者，每秒发送指定数量的消息"""
    try:
        # 创建生产者实例
        producer = KafkaProducer(
            bootstrap_servers=KAFKA_BROKER,
            value_serializer=lambda v: json.dumps(v).encode('utf-8'),  # 序列化消息为JSON
            linger_ms=5,  # 等待5ms再发送，用于批量处理
            batch_size=16384  # 批量大小
        )

        print(f"开始发送消息，每秒{str(MESSAGES_PER_SECOND)}条，目标主题: {TOPIC_NAME}")
        print(f"运行时长: {'无限' if RUN_DURATION == 0 else f'{RUN_DURATION}秒'}")
        print("按Ctrl+C停止...")

        message_id = 1
        start_time = time.time()
        end_time = start_time + RUN_DURATION if RUN_DURATION > 0 else float('inf')

        # 计算每条消息之间的间隔时间(秒)
        interval = 1.0 / MESSAGES_PER_SECOND

        while time.time() < end_time:
            # 记录批次开始时间
            batch_start = time.time()

            # 创建并发送消息
            message = create_message(message_id)
            producer.send(TOPIC_NAME, value=message)

            # 每1000条消息打印一次进度
            if message_id % 1000 == 0:
                elapsed = time.time() - start_time
                rate = message_id / elapsed if elapsed > 0 else 0
                print(f"已发送 {message_id} 条消息，当前速率: {rate:.2f}条/秒")

            message_id += 1

            # 控制发送速率
            elapsed = time.time() - batch_start
            if elapsed < interval:
                time.sleep(interval - elapsed)

        # 确保所有消息都被发送
        producer.flush()
        print(f"发送完成，共发送 {message_id - 1} 条消息")

    except KeyboardInterrupt:
        print("\n用户中断发送")
        # 确保已发送的消息被处理
        if 'producer' in locals():
            producer.flush()
        print(f"已发送 {message_id - 1} 条消息")
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
        message_count = 0
        start_time = time.time()

        # 消费消息
        for message in consumer:
            message_count += 1

            # 每100条消息打印一次统计信息
            if message_count % 100 == 0:
                elapsed = time.time() - start_time
                rate = message_count / elapsed if elapsed > 0 else 0
                print(f"已接收 {message_count} 条消息，消费速率: {rate:.2f}条/秒")

    except KeyboardInterrupt:
        print(f"\n用户中断消费，共接收 {message_count} 条消息")
    except Exception as e:
        print(f"消费者错误: {str(e)}")
    finally:
        if 'consumer' in locals():
            consumer.close()


if __name__ == "__main__":
    import sys

    # 允许通过命令行参数选择运行生产者还是消费者
    if len(sys.argv) > 1 and sys.argv[1] == 'consumer':
        print("=== 启动消费者 ===")
        kafka_consumer()
    else:
        print("=== 启动高速生产者 ===")
        kafka_high_speed_producer()
