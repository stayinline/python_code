dict_a = {'name': 'bob', 'age': 12}
print(dict_a)  # {'name': 'bob', 'age': 12}

dict_b = {'name': 'bob', 'name': 'alice'}
print(dict_b)  # {'name': 'alice'}

dict_c = {'name1': 'bob', 'name2': 'alice'}
print(dict_c)  # {'name1': 'bob', 'name2': 'alice'}

dict_a = {'name': 'bob', 'age': 12}
# print(dict_a[1])  # KeyError: 1
# print(dict_a('name'))  # TypeError: 'dict' object is not callable
print(dict_a['name'])  # bob
# print(dict_a['head'])  # KeyError: 'head'

print('-------------------------')
dict_a = {'name': 'bob', 'age': 12}
print(dict_a.get(1))  # None
print(dict_a.get('name'))  # bob
print(dict_a.get('head', '不存在'))  # 不存在

print('-------------------------')
dict_a = {'name': 'bob', 'age': 12}
dict_a['name'] = 'alice'
print(dict_a)  # {'name': 'alice', 'age': 12}
dict_a['head'] = 'h1'
print(dict_a)  # {'name': 'alice', 'age': 12, 'head': 'h1'}

print('-------------------------')
dict_a = {'name': 'bob', 'age': 12}
del dict_a
# print(dict_a)  # NameError: name 'dict_a' is not defined. Did you mean: 'dict_b'?

dict_a = {'name': 'bob', 'age': 12}
del dict_a['age']
# del dict_a['head'] #KeyError: 'head'
print(dict_a)  # {'name': 'bob'}

dict_a = {'name': 'bob', 'age': 12}
dict_a.clear()
print(dict_a)  # {}

dict_a = {'name': 'bob', 'age': 12}
dict_a.pop('age')
# dict_a.pop('head') #KeyError: 'head'
print(dict_a)  # {'name': 'bob'}

dict_a = {'name': 'bob', 'age': 12}
# dict_a.pop()  # TypeError: pop expected at least 1 argument, got 0


dict_a = {'name': 'bob', 'age': 12}
print(len(dict_a))  # 2
print(dict_a.keys())  # dict_keys(['name', 'age'])
print(type(dict_a.keys()))  # <class 'dict_keys'>

print(dict_a.values())  # dict_values(['bob', 12])
print(type(dict_a.values()))  # <class 'dict_values'>

print(dict_a.items()) # dict_items([('name', 'bob'), ('age', 12)])
print(type(dict_a.items()))  # <class 'dict_items'>

