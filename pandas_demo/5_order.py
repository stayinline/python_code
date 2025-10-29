import pandas as pd
import numpy as np  # 用于处理可能的除零问题

# 修正数据读取（使用read_excel读取xlsx文件）
file_name = r"D:\code\python\pandas_demo\file\sales_data.xlsx"
df = pd.read_csv(file_name)
print("原始数据形状：", df.shape)


# 假设已完成之前的清洗步骤（缺失值填充、去重、销售额转浮点数等）
# 此处补充清洗后的处理：

# 1. 按"销售额"降序排序，取前10条订单
top10_sales = df.sort_values(by="sales", ascending=False).head(10)
print("\n1. 销售额前10的订单：")
print(top10_sales[["order_id", "product_category", "sales"]])  # 展示关键列


# 2. 按"商品类别"分组，计算每组的平均销量、总销售额
category_stats = df.groupby("product_category").agg(
    平均销量=("quantity", "mean"),  # 计算每组销量的平均值
    总销售额=("sales", "sum")   # 计算每组销售额的总和
).reset_index()  # 将分组列"商品类别"从索引转为普通列
print("\n2. 各商品类别的统计数据：")
print(category_stats)


# 3. 新增"客单价"列（客单价=销售额/销量）
# 注意：需处理销量为0的情况（避免除零错误，转为NaN）
df["客单价"] = df["sales"] / df["quantity"]
# 将除零导致的无穷大(inf)转为NaN
df["客单价"] = df["客单价"].replace([np.inf, -np.inf], np.nan)
print("\n3. 新增客单价列后（部分数据）：")
print(df[["order_id", "sales", "quantity", "客单价"]].head())
