class Student:
    pass
class Person:
    pass

def main():
    print(type(Student))
    print(type(Person))
    print(isinstance(Student,type))#类本身也是一个对象，是 type类型的对象
    print(Student)
    student_1 = Student()

    print(student_1)
    print(hex(id(student_1)))
    print(isinstance(student_1,Student))
    print(isinstance(student_1,Person))
    student_2 = Student()
    print(student_2)
    print(isinstance(student_2,Student))

if __name__ == '__main__':

    main()