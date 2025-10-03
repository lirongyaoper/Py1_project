#什么是类变量
    # 属于类本身这个对象的属性
    # 所有该类的对象都共享类变量
# 定义类变量
# 取得类变量的之
# 设置类变量的值
# 删除类变量
# 类变量的存储

class Student:
    student_count =0#类变量


def main():
    print(Student.__name__)
    print(Student.student_count)
    print(getattr(Student,"student_count"))
    print(getattr(Student,'unknow','20'))
    #直接设置类变量的值
    Student.student_count = 100
    print(Student.student_count)
    # 使用setattr在()函数设置类变量的值
    setattr(Student,'student_count',200)
    print(Student.student_count)
    #如果类变量不存在，可以在运行时动态添加
    Student.unknown="hello"
    print(Student.unknown)
    #删除类变量方法一
    # del Student.unknown
    #删除类变量方法二
    # delattr(Student,'student_count')
    # print(Student.unknown)
    # print(Student.student_count)
    s1 = Student()
    s2 = Student()
    print(s1.student_count)
    print(s2.student_count)
    print(Student.__dict__)



if __name__ == '__main__':
    main()
