import pandas as pd
import numpy as np
import matplotlib.pyplot as plt  # 用于绘图

# 设置中文显示（避免图表中文乱码）
plt.rcParams["font.family"] = ["SimHei", "WenQuanYi Micro Hei", "Heiti TC"]

# 1. 读取数据（请替换为你的文件实际路径）
file_name = r"D:\code\python\pandas_demo\file\titanic.csv"  # 注意路径正确性
df = pd.read_csv(file_name)
print("原始数据形状：", df.shape)

# print(df.head(3))

# 查看缺失值信息（重点关注"age"列）
print("\n1. 数据缺失值信息：")
df.info()  # 此时会显示实际列名（小写）

# 2. 数据预处理
# 填充"age"缺失值为全体乘客均值（列名为小写age）
df['age'].fillna(df['age'].mean(), inplace=True)
# 删除"cabin"列（列名为小写cabin，缺失值过多）
df.drop('cabin', axis=1, inplace=True)  # axis=1表示删除列

# 验证处理结果
print("\n2. 处理后的数据缺失值信息：")
df.info()  # 可观察到age列无缺失，cabin列已删除

# 3. 按性别分组计算生存率（列名为sex和survived，均为小写）
sex_survival_rate = df.groupby("sex")["survived"].mean()
print("\n3. 按性别分组的生存率：")
print(sex_survival_rate)
# 转换为百分比显示（更直观）
print("\n百分比形式：")
print(sex_survival_rate.apply(lambda x: f"{x * 100:.2f}%"))

# 4. 绘制性别生存率对比图
plt.figure(figsize=(8, 5))  # 设置图表大小
sex_survival_rate.plot(kind="bar", color=['lightcoral', 'skyblue'])
plt.title("泰坦尼克号不同性别的生存率对比", fontsize=15)
plt.xlabel("性别", fontsize=12)
plt.ylabel("生存率", fontsize=12)
plt.xticks(rotation=0)  # x轴标签横向显示
plt.ylim(0, 1)  # y轴范围设置为0-1（符合生存率范围）
plt.grid(axis='y', linestyle='--', alpha=0.7)  # 添加y轴网格线
plt.show()

# 5. 保存为ipynb文件说明
print("\n5. 保存说明：请在Jupyter Notebook中运行上述代码，完成后通过菜单栏 "
      "'File -> Save and Checkpoint' 保存，文件名设置为 'titanic_survival_analysis.ipynb' 即可。")
