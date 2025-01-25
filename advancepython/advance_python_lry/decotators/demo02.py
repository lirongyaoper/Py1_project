import time
def foo():
    time.sleep(3)
    print('in foo')

def gf(func):
    start_time = time.time()
    func()
    end_time = time.time()
    print('运行的世时间为： ',end_time - start_time)
gf(foo)
