from OOP_Python_lry.Descriptor.student_1 import Student1
from OOP_Python_lry.Descriptor.student_2 import Student2



def main():
    # student_1 = Student1("jack", "Ma")
    # student_1.last_name = ""

    student_2 = Student2()
    student_2.first_name = "jack"
    student_2.last_name = "   w"
    print(student_2.first_name)
    print(student_2.last_name)

    print("***************************************")
    student_3 = Student2()
    student_3.first_name = "tom"
    print(student_3.first_name)

if __name__ == '__main__':
    main()