class Student:
    def __init__(self,name,age):
        self.name = name
        self.__age = age
    def say_hello(self,msg):
        print(f"Hello {msg},{self.name}今年{self.__age}岁了")
def main():
    s1 = Student("jack",40)
    print(s1.say_hello("qinaide"))
    print(s1._Student__age)  # _classname__attribute
    print(s1.__age) #c错误

if __name__ == '__main__':
    main()