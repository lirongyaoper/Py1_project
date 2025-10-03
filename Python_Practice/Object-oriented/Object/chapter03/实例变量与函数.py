"""
掌握：
    实例函数的定义
    认识__init__函数
    定义实例变量  在__init__()函数中定义实例变量
    实例函数中访问实例变量
    外部访问实例变量与函数
"""


class Student:
    student_count = 10
    #实例函数
    def __init__(self,name,age):
        #实例变量
        self.name = name
        self.age = age
    # 实例函数的定义
    def say_hello(self, msg):
        print(f"hello{msg},{self.name}")

def main():
    #1.create a physical object
    #2. call __init__() to initialize this object
    student1 = Student("shaohehuan",22)
    student1.say_hello("rongyao")



if __name__ == '__main__':
    main()