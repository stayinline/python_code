import pandas as pd


data = {
    '姓名': ['张三', '李四', '王五', '赵六'],
    '年龄': [25, 30, 35, 28],
    '城市': ['北京', '上海', '广州', '深圳'],
    '工资': [15000, 18000, 12000, 16000]
}
df = pd.DataFrame(data)

# 2. 查看DataFrame信息
print(df.head(2))     # 前2行
print(df.tail(2))     # 后2行
print(df.shape)       # 形状
print(df.describe())  # 统计描述