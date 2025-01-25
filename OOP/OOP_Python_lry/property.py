"""
如何防止实例变量被外部错误修改 编写 setter 和 getter 方法  引入 property 类
"""

class Student:
    def __init__(self,name:str,age: int):
        self.name = name
        self.__age = age


    def set_age(self,age:int):
        if age <0 or age > 150:
            raise Exception(f"Age {age} is not valid")
        self.__age = age

    def get_age(self):
        return self.__age


    age = property(fget=get_age,fset=set_age)


    def __str__(self):
        return f"{self.name},{self.__age}"

def main():
    student = Student("lizhi",20)
    student.age = 5
    print(student.age)
    student.set_age(3)


    print(student.get_age())

if __name__ =='__main__':
    main()
