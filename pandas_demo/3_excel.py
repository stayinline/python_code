import pandas as pd


# 读取 csv
file_name = "D:\download\oss_68bfe799b84644bc6ef140e6_keys.csv"
df = pd.read_csv(file_name, encoding="utf-8-sig")
print(df)

print(type(df))



# 保存成csv
sut_data = {
    '姓名': ['Bob', 'Alice', 'Alen'],
    '年龄': [10, 10, 12],
    '成绩': [99.1, 92, 80],

}

s2 = pd.DataFrame(sut_data)
print(s2)

save_path = r'D:\code\python\pandas_demo\file\excellent_students.csv'

s2[s2["成绩"] > 90].to_csv(
    save_path,
    index=False,  # 不保存DataFrame的索引列
    encoding="utf-8-sig"  # 确保中文正常写入
)

print("\n优秀学生数据已保存为 excellent_students.csv")
