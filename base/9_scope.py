# a = 10
#
#
# def func():
#     a = 2
#     print("在 函数 func 内部时，a=", a)
#
#
# func()
#
# print('a=', a)


a = 10

print("初始定义时，a=", a)


def func():
    global a
    a = 2
    print("在 函数 func 内部时，a=", a)


func()

print('a=', a)
