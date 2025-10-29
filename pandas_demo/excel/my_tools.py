
import random
from datetime import time


def generate_random_long_like_timestamp():
    # 创建随机数生成器实例
    rand = random.Random()

    # 获取当前毫秒级时间戳（作为基础值，类似时间戳特性）
    current_millis = int(time.time() * 1000)

    # 定义随机偏移范围（例如：±1天的毫秒数，可根据需求调整）
    one_day_millis = 24 * 60 * 60 * 1000  # 86400000毫秒
    min_offset = -one_day_millis  # 最小偏移：-1天
    max_offset = one_day_millis  # 最大偏移：+1天

    # 生成指定范围内的随机偏移量（整数）
    offset = rand.randint(min_offset, max_offset)

    # 计算最终结果（确保为正数，符合时间戳特性）
    result = current_millis + offset
    return result if result >= 0 else -result  # 避免负数
