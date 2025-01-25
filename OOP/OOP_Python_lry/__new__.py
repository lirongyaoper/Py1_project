


def execute(*args,**kwargs):
    print(args)
    print(kwargs)



"""
__new__方法的执行时刻
构造一个对象的过程，比如：
person = Person("Hack")
    1. person =object.__new__(Person,"Hack")
    2. person.__init__("Hack")
"""
class  SquareNumber(int):
    def __new__(cls, value:int):
        return super().__new__(cls,value **2)


class Student:
    def __new__(cls,first_name,last_name):
        obj = super().__new__(cls)
        obj.first_name = first_name
        obj.last_name = last_name
        return obj






def main():
    execute("cxj")
    execute("abc","p1","p2",2,name = "lirongyao",age = 55)
    execute("abc",23)

    num = SquareNumber(2)
    print(num)
    print(type(num))
    print(isinstance(num,int))
    srudent1 = Student("li","rongao")
    print(srudent1.last_name)
    print(srudent1.first_name)





if __name__== '__main__':
    main()