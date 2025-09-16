# def func():
#     print("这是函数体")
#
#
# func()
#
#
# def func2():
#     print("这是函数体")
#     return "有返回值"
#
#
# var = func2()
# print(var)
# print(type(var))
#
#
# def func3():
#     print("这是函数体")
#     return "有返回值",123
#
# var3 = func3()
# print(var3)
# print(type(var3))


def func():
    print("这是函数体")

    def func_inline():
        print("这是内嵌函数")

    func_inline()


func()
