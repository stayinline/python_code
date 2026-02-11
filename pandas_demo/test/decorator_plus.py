# 定义日志器类
class EventLogger:
    def __init__(self, level="INFO"):
        self.level = level  # 日志级别，可自定义

    # 定义作为装饰器的方法
    def log_this(self, func):
        def wrapper(*args, **kwargs):
            # 增强逻辑：打印日志（使用对象的level属性）
            print(f"[{self.level}] 方法 {func.__name__} 被调用，参数：{args}, {kwargs}")
            result = func(*args, **kwargs)
            print(f"[{self.level}] 方法 {func.__name__} 执行结束")
            return result

        return wrapper


# 创建EventLogger的实例（可配置日志级别）
event_logger = EventLogger(level="DEBUG")


# 使用对象方法作为装饰器
@event_logger.log_this
def multiply(a, b):
    return a * b


# 调用被装饰的方法
multiply(3, 4)