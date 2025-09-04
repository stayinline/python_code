s = 'hello'

print(type(s))

a = s.encode()
print(a)
print(type(a))
print(a.decode())  # hello

print('hello' + ' ' + 'python')  # hello python

print('s' in s) #False
print('h' in s) #True
print('c' not in s) #True


s = 'hello'

print(s[0]) #h
print(s[1]) #e
print(s[2]) #l
print(s[3]) #l
print(s[4]) #o
#print(s[6]) #报错 IndexError: string index out of range

s = 'hello'
print(s[0:2:1]) #he
print(s[2])     #l
print(s[2:])    #llo
print(s[:3])    #hel




