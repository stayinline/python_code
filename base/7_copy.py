# li = [1, 2, 3, 4]
# li2 = li
# print("li=", li)
# print("li2=", li2)
# li.append(55)
# print("li=", li)
# print("li2=", li2)
# print("li 地址=", id(li))
# print("li2 地址=", id(li2))


import copy

li = [1, 2, 3, [4, 5, 6]]
li2 = copy.copy(li)
print("li=", li)
print("li2=", li2)
li[3].append(55)
print("li=", li)
print("li2=", li2)
print("li 地址=", id(li))
print("li2 地址=", id(li2))

#
# import copy
#
# li = [1, 2, 3, [4, 5, 6]]
# li2 = copy.deepcopy(li)
# print("li=", li)
# print("li2=", li2)
# li[3].append(55)
# print("li=", li)
# print("li2=", li2)
# print("li 地址=", id(li))
# print("li2 地址=", id(li2))
