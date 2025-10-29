import pandas as pd

# 读取 csv
# file_name = "D:\code\python\pandas_demo\file\titanic.csv" 这种在Windows环境会报错，解析不了这种格式的路径
file_name = r"D:\code\python\pandas_demo\file\titanic.csv"
df = pd.read_csv(file_name, encoding="utf-8-sig")
print(df)

print(df.head(6))


print(df.groupby("sex"))




file_name = r"D:\code\python\pandas_demo\file\sales_data.xlsx"
df = pd.read_csv(file_name, encoding="utf-8-sig")
print(df)


# 1. 统计各列缺失值数量
print("\n1. 各列缺失值数量：")
missing_values = df.isnull().sum()  # isnull()标记缺失值，sum()统计每列缺失值
print(missing_values)


# 2. 用"商品类别"分组，填充"销量"列的缺失值为该组均值
# 分组后用transform计算每组均值并填充缺失值
df['quantity'] = df.groupby('product_category')['quantity'].transform(
    lambda x: x.fillna(x.mean())  # 对每组的"销量"缺失值填充该组均值
)
print("\n2. 填充销量缺失值后（部分数据）：")
print(df[['product_category', 'quantity']].head())  # 查看填充效果


# 3. 删除"订单号"重复的行
# drop_duplicates 默认保留第一个重复行，subset指定按"订单号"去重
df = df.drop_duplicates(subset='order_id', keep='first')
print("\n3. 删除重复订单号后的数据形状（行,列）：", df.shape)  # 查看去重后的数据量


# 4. 将"销售额"列从字符串型转为浮点数型（修正版）
# 步骤1：确认列名正确（这里假设列名是“销售额”，如果是“sales”请替换）
column_name = "sales"  # 确保与实际列名一致

# 步骤2：检查并转换该列为字符串类型（避免非字符串类型导致.str报错）
df[column_name] = df[column_name].astype(str)

# 步骤3：清除字符串中可能的非数字字符（如￥、逗号、空格等）
df[column_name] = df[column_name].str.replace(r'[^\d.]', '', regex=True)

# 步骤4：转换为浮点数（用pd.to_numeric更安全，错误值会转为NaN）
df[column_name] = pd.to_numeric(df[column_name], errors='coerce')

# 验证结果
print(f"\n4. 转换后{column_name}列的数据类型：", df[column_name].dtype)
print(df[column_name].head(3))
