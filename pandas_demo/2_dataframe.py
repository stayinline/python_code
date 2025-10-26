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



print("Pandas版本：", pd.__version__)

s1 = pd.Series({"北京": 24, "上海": 22, "天津": 22, "河北": 23, "南京": 24})
print(s1)

# 北京    24
# 上海    22
# 天津    22
# 河北    23
# 南京    24
# dtype: int64

sut_data = {
    '姓名': ['Bob', 'Alice', 'Alen'],
    '年龄': [10, 10, 12],
    '成绩': [99.1, 92, '未知']
}

s2 = pd.DataFrame(sut_data)
print(s2)

#    姓名  年龄    成绩
# 0    Bob  10  99.1
# 1  Alice  10  92.3
# 2   Alen  12  未知


# 1. 查看前n行（默认前5行，这里3行数据会全显示）
print("head()查看前几行：")
print(s2.head(2))  # 也可指定行数，如head(2)只看前2行

#       姓名  年龄    成绩
# 0    Bob  10  99.1
# 1  Alice  10    92

# 2. 查看数据基本信息（数据类型、非空值等）
print("\ninfo()查看数据信息：")
print(s2.info())

# <class 'pandas.core.frame.DataFrame'>
# RangeIndex: 3 entries, 0 to 2
# Data columns (total 3 columns):
#  #   Column  Non-Null Count  Dtype
# ---  ------  --------------  -----
#  0   姓名      3 non-null      object
#  1   年龄      3 non-null      int64
#  2   成绩      3 non-null      object
# dtypes: int64(1), object(2)
# memory usage: 204.0+ bytes
# None


# 3. 查看行列数（元组：(行数, 列数)）
print("\nshape查看行列数：")
print(s2.shape)

# (3, 3)

# 行列处理
print(s1)
print("城市气温第一行：")
print(s1.iloc[0])

print("城市气温第一列：")
print(s1['北京'])

print(s2)
print("学生数据第一行：")
print(s2.iloc[0])  # iloc 中的 i 就是index，表示下边
print(s2.loc[0])

print("学生数据第一列：")
print(s2["姓名"])
# 0      Bob
# 1    Alice
# 2     Alen
# Name: 姓名, dtype: object


# excellent_stu = s2[s2["成绩"] > 85]
# 由于成绩中有汉字“未知”，这事直接比较符操作，会导致不支持的报错
#    姓名  年龄    成绩
# 0    Bob  10  99.1
# 1  Alice  10  92.3
# 2   Alen  12  未知
s2.loc[2, '成绩'] = 78  # 修改编号为2 的“成绩”这个值

# 下面这种写法会报错
# if s2["成绩"] > 85:
#     print("优秀")

print(type(s2["成绩"] > 85))  # <class 'pandas.core.series.Series'>

# if (s2["成绩"] > 85).any(): # 任一
if (s2["成绩"] > 85).all():  # 全部
        print( "优秀")
