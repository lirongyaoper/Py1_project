
"""
一 . 引言
    1.1 Python的迭代机制依赖于两个特殊方法：iter__和__next。__iter__方法返回一个迭代器对象，而__next__方法则负责返回迭代器的下一个值。当没有更多的值可返回时，__next__会抛出StopIteration异常。这使得Python中的所有可迭代对象都可以被自然地用于for循环。
    1.2
"""
# def fibonacci():
#     a , b = 0 , 1
#     while True:
#         yield  a
#         a , b = b , a+b
# for num in fibonacci():
#     if num >100:
#         break
#     print(num)

print("*******************************************************************")

# class SimpleIterator:
#     def __init__(self,limit):
#         self.limit = limit
#         self.current = 0
#     def __iter__(self):
#         return self
#     def __next__(self):
#         if self.current >= self.limit:
#             raise StopIteration
#         value = self.current
#         self.current += 1
#         return value
#
# it = SimpleIterator(5)
# for i in it:
#     print(i)
print("*******************************************************************")
# my_list = [1,2,3]
# my_iterator = iter(my_list) #my_list 必须是可迭代的对象
# print(next(my_iterator))
# print(next(my_iterator))
# print(next(my_iterator))
print("*******************************************************************")

# class MyNumerSequenceIterator:
#     def __init__(self,start,end):
#         self.current  = start
#         self.end = end
#     def __iter__(self):
#         return self
#     def __next__(self):
#         if self.current >= self.end:
#             raise StopIteration
#         result =self.current
#         self.current += 1
#         return result
#
# seq_iter = MyNumerSequenceIterator(1,20)
# for num in seq_iter:
#     print(num)

print("****************************生成器表达式***************************************")
squares = (x**2 for x in range(20))
for square in squares:
    print(square)

import sys
large_list =  [i for i in range(1000000)]
large_iter = (i for i in range(1000000))
print(sys.getsizeof(large_list))
print(sys.getsizeof(large_iter))
