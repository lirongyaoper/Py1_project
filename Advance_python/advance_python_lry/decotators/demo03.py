import time

def timer(func):
    def gf():
        start_time = time.time()
        func()
        end_time = time.time()
        print('func运行时间为：',end_time - start_time)
    return gf

@timer
def foo():
    time.sleep(3)
    print('in foo')
foo()