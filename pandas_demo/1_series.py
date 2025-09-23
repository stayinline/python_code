# 实战任务
import pandas as pd
import numpy as np

# 1. 创建不同类型的 Series
# 语法：s = pd.Series(data, index=index)

# index 可以省略
s1 = pd.Series([1, 3, 5, np.nan, 6, 8])
print(s1)

s = pd.Series(np.random.randn(5), index=["a", "b", "c", "d", "e"])
print("s=")
print(s)

# s=
# a   -0.346642
# b   -0.703765
# c   -0.217754
# d   -1.151748
# e   -0.572207
# dtype: float64

print(s.index)
# Index(['a', 'b', 'c', 'd', 'e'], dtype='object')

print("############")

# 方式二：从 dict 中创建
dict_a = {'A': 'a', 'B': 'b', 'C': 'c', 'D': 'd'}
s2 = pd.Series(dict_a)
print(s2)

# 这里要注意，前面是index，后面是value
# A    a
# B    b
# C    c
# D    d
# dtype: object

# 方式四：用常量创建
s3 = pd.Series(5.0, index=["a", "b", "c", "d", "e"])
print(s3)
#
# a    5.0
# b    5.0
# c    5.0
# d    5.0
# e    5.0
# dtype: float64

print("############")

# 2. Series基本操作
s = pd.Series(np.random.randn(5), index=["a", "b", "c", "d", "e"])
print(s)

print(s.iloc[0])  # index获取
print(s.iloc[:3])  # 数组的类似操作
print(s[s > s.median()])  # 条件判断
print(s.iloc[[4, 3, 1]])  # 乱序指定 index
print("############")
#
# a   -0.131554
# b    1.871958
# c    0.876683
# d   -0.694043
# e   -1.412106
# dtype: float64
# -0.13155410450673252
# a   -0.131554
# b    1.871958
# c    0.876683
# dtype: float64
# b    1.871958
# c    0.876683
# dtype: float64
# e   -1.412106
# d   -0.694043
# b    1.871958
# dtype: float64


# 方便快捷的操作
s = pd.Series(np.random.randn(5), index=["a", "b", "c", "d", "e"])
print(s)

print(s + s)
print(s * 2)

# 3、把pandas的 series 转换成  numpy
n = np.exp(s)
print(n)
print(type(n))
print(type(s))
print("#######歌手发歌单了#####")

# 注意：这里还没有转换成功
# a    0.287885
# b    6.853385
# c    1.048381
# d    3.733064
# e    0.287346
# dtype: float64
# <class 'pandas.core.series.Series'>
# <class 'pandas.core.series.Series'>

# 以下才是正确的转换方式
np1 = s.to_numpy()
print(np1)
print(type(np1))

# [-1.24519576  1.92474275  0.04724665  1.31722946 -1.24706677]
# <class 'numpy.ndarray'>
print("############")

# 4、命名series
s = pd.Series(np.random.randn(5), name="something")
print(s)

# 0    1.620540
# 1    0.519225
# 2   -0.471130
# 3   -0.866819
# 4   -0.614206
# Name: something, dtype: float64
s.rename("qwer") # 这是不生效的
s_new= s.rename("qwer")
print(s_new)

# 0   -1.588934
# 1    0.463822
# 2   -0.296469
# 3    0.033627
# 4   -0.765221
# Name: qwer, dtype: float64