s1 = {1, 2, 33, 4}
print(s1)  # {1, 2, 4, 33}
print(type(s1))  # <class 'set'>

s1 = set()
print(s1)  # {}

# 集合具有无序性
s1 = {'a', 'b', 'c', 'd', 'e'}
print(s1)
# 第一次运行：{'e', 'b', 'a', 'c', 'd'}
# 第二次运行：{'e', 'd', 'b', 'a', 'c'}
print('-------------------------')

# 添加
s1 = {1, 2, 33, 4}
s1.add(5)
# s1.add(6, 7) # TypeError: set.add() takes exactly one argument (2 given)
print(s1)  # {1, 2, 33, 4, 5}

# update 里面必须是可迭代对象
# s1.update(6) # TypeError: 'int' object is not iterable
s1.update({6, 7})
print(s1)  # {1, 2, 33, 4, 5, 6, 7}
s1.update((8, 9))
print(s1)  # {1, 2, 33, 4, 5, 6, 7, 8, 9}

# 删除
print('-------------------------')
s1 = {1, 2, 33, 4}
# s1.remove(6) # KeyError: 6
s1.remove(33)  # KeyError: 6
print(s1)  # {1, 2, 4}

s1.pop()
# s1.pop(2) # TypeError: set.pop() takes no arguments (1 given)
print(s1)  # {2, 4}

print('-------------------------')
s1 = {1, 2, 33, 4}
s1.discard(33)
s1.discard(7)  # 不报错，无效
print(s1)  # {1, 2, 4}

print('---------交集----------------')
s1 = {1, 2, 33, 4}
s2 = {4, 5, 6, 1}
s3 = {7, 8}
print(s1 & s2)  # {1, 4}
print(s1 & s3)  # set()
print(type(s1 & s3))  # <class 'set'>

print('---------并集（会去重）----------------')
s1 = {1, 2, 33, 4}
s2 = {4, 5, 6, 1}
print(s1 | s2)  # {1, 2, 33, 4, 5, 6}
print(type(s1 & s2))  # <class 'set'>


