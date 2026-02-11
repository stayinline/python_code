# 定义一个日志装饰器函数
def log_this(func):
    # 定义包装函数，增强原函数的行为
    def wrapper(*args, **kwargs):
        print(f"[日志] 函数 {func.__name__} 开始执行")
        # 执行原函数并获取返回值
        result = func(*args, **kwargs)
        print(f"[日志] 函数 {func.__name__} 执行完成，返回值：{result}")
        return result
    # 返回包装后的函数
    return wrapper

# 使用装饰器（@语法糖）
@log_this
def add(a, b):
    return a + b

# 调用被装饰的函数
add(1, 2)