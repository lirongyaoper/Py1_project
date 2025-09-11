"""
一个metaclass 就是一个用来创建其他class的类
type 就是所有类默认的metaclass
你可以在定义类的时候制定metaclass
"""
class Human(type):
    @staticmethod
    def __new__(cls, *args,**kwargs):
        class_ = super().__new__(cls,*args)

        if kwargs:
            for name,value in kwargs.items():
                setattr(class_,name,value)
        return class_





class Student(object,metaclass=Human,country="China",freedom = True):
    pass

print(Student.country)
print(Student.freedom)
