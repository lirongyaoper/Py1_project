def outer(func):
    print("outer()函数开始执行")

    def inner(*args,**kwargs):
        print("inner()函数开始执行了")
        result = func(*args,**kwargs)
        print("inner（）函数执行结束可")
        return result

    print("outer()函数执行结束了")

    return inner

@outer
def f():
    print("f()函数执行了")

f()
