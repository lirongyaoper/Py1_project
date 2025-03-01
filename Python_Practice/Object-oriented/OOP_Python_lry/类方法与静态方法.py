# class Student:
#     school = "abc"
#
#     @classmethod
#     def get_instance(cls):
#         return cls()
#
# student = Student.get_instance()
print("****************************类方法*********************************")

# class Student:
#     student = "aaa"
#     @classmethod
#     def get_instance(cls):
#         print(cls.__name__)
#         print(cls.student)
#
# def main():
#     Student.get_instance()
#     print(Student.__name__)
#     print(Student.student)
#
#
# if __name__ == '__main__':
#     main()

print("**************************静态方法***********************************")


class Student:
    student = "aaa"
    @classmethod
    def get_instance(cls):
        print(cls.__name__)
        print(cls.student)

    @staticmethod
    def out():
        print(f"hello {Student.student}")
    @staticmethod
    def size(value:int)-> float:
        return value *1.5

    def speak(self):             #实力列方法中调用静态方法
        n =12
        n = self.size(n)
        print(n)

def main():
    Student.get_instance()#类方法的调用
    print(Student.__name__)
    print(Student.student)
    Student.out()  #静态方法的调用
    Student().speak()##实例方法的调用


if __name__ == '__main__':
    main()