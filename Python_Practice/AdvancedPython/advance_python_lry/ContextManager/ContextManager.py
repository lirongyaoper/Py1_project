"""
上下文管理器：
1.  协议
    一个上下文管理器需要实现如下方法：
        __enter__() 安装上下文，可以返回对象
        __exit__()  清除（释放）对象
2. 应用
    开---关
    锁---释放
    启动---停止
    改变---重置

"""


import time
class Timer:
     def __init__(self):
         self.elapsed = 0

     def __enter__(self):
         self.start = time.perf_counter()
         return self

     def __exit__(self, exc_type, exc_val, exc_tb):
         self.stop = time.perf_counter()
         self.elapsed = self.stop - self.start


with Timer() as timer:  #timer 所指的对象为__enter__方法的返回值  重点
    nums = []
    for n in range(10000):
        nums.append(n **2 )

print(timer.elapsed)