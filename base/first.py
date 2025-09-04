#
#
# #print("hello python")
#
# a=100
#
# a='sfasf'
#
# print(a)
#
# a=1.5
# print(a)
#
#
# print(True)
#
# print(False)
#
#
# str='test'
#
# str="test"
# print(str)
#
# str='''
# select
# *
# from table_a
# where id > 10
# '''
#
# sql="""
# select
# *
# from table_a
# where id > 10
# """
#
# print(str)
# print(sql)
#
#
#

a = 21

if a < 10:
    print("a < 10")

if a < 10:
    print("a < 10")
else:
    print("a >= 10")

if a < 10:
    print("a < 10")
elif a < 20:
    print("10 < a < 20")

else:
    print("a >= 20")

i = 0
while i < 5:
    print("test")
    i += 1

str = 'hello'
for i in str:
    print(i)

for i in range(1, 5):
    print(i)

sum = 0
for i in range(1, 101):
    sum += i
print(sum)

str = 'hellopython'
i = 0
while True:
    if (i < 5):
        print(str[i])
        i += 1
    else:
        print("长度大于5，退出")
        break
