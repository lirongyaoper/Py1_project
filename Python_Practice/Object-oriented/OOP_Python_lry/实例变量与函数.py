class Student:
    def __init__(self,name,age):
        self.name = name
        self.age = age
    def say_hello(self,msg):
        print(f"Hello {msg},{self.name}今年{self.age}岁了")

def main():
    s1 = Student("lirongyao",33)
    s2 = Student("cuixiuhuan",33)
    s1.say_hello("tonzhimen")
    s2.say_hello("woainimen")
    s1.gender ='Male'
    print(s1.gender)
    #print(s2.gender)

if __name__ == '__main__':
    main()