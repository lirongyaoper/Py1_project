"""
任何class 在内存中就是一个type类的对象
Python使用type类来创建其他的class
    type(class_name,parents,class_dict)
理论上讲，可以使用type来动态创建class
"""


# from lief import Object
#
#
# class Student:
#     def greeting(self):
#         print("hello student")
# print(type(Student))#<class 'type'>
# print(isinstance(Student,type))#True
# print(isinstance(Student,Object))#False

print("*************************************************************")

class_body = """
def greeting(self):
    print("Hello customer")
def jump(self):
    print('jump')
"""
class_dict ={}
exec (class_body,globals(),class_dict) #把文本内容转化为Python字典

Customer=type("Customer",(object,),class_dict)

c = Customer()
c.greeting()



