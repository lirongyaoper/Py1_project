import time


def timer(timer_type):
    print(timer_type)
    def outer(func):
        def inner(*args,**kwargs):
            start_time = time.time()
            res = func(*args,**kwargs)
            end_time = time.time()
            print('func函数的运行时间为： ',end_time - start_time)
            return res
        return inner
    return outer


@timer(timer_type='minites')
def foo(name, age):
    time.sleep(3)
    print('in foo',name,age)
    return name


print(foo('mouniu',23))