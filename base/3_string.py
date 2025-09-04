s = 'hello python'
print(s.find('llo'))  # 2
print(s.find('h'))  # 0 --第一个 h 下标为0，所以返回0
print(s.find('h', 2))  # 9
print(s.find('java'))  # -1
print(s.find('l', 1, 4))  # 2

print('----------------')
s = 'hello python'
print(s.index('llo'))  # 2
print(s.index('h'))  # 0 --第一个 h 下标为0，所以返回0
print(s.index('h', 2))  # 9
# print(s.index('java'))    # 报错：ValueError: substring not found
print(s.index('l', 1, 4))  # 2

print('----------------')
s = 'hello python'
print(s.startswith('he'))  # True
print(s.startswith('oe'))  # False
print(s.startswith('py', s.find('p'), 10))  # True

print('----------------')
s = 'hello python'
print(s.islower())  # True
print(s.isupper())  # False
print(s.lower())  # hello python
print(s.upper())  # HELLO PYTHON


s = '1234'
print(s.isdigit())  # True
print(s.isnumeric())  # True

print('----------------')
s = 'hello python'
print(s.replace('h', '-'))  # -ello pyt-on
print(s.replace('h', '-', 1))  # -ello python

print('----------------')
s = 'hello python'
print(s.split(' '))  # ['hello', 'python']
print(s.split(','))  # ['hello python']
s = 'hello python script'
print(s.split(' ',1))  # 只切分一次 ['hello', 'python script']

