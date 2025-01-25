from sympy import false


class MyDate:
    def __init__(self,year,month,day):
        self.year = year
        self.month = month
        self.day = day

    def __str__(self):
        print("str is called!")
        return f"{self.year}-{self.month}-{self.day}"

    def __repr__(self):   #用于返回一个描述对象本身的字符串，该描述的主要目标是机器或者开发者
        print("repr is called")
        return f"MyDate:{self.year}-{self.month}-{self.day}"
    def __eq__(self, other):
        print("ed is called ")
        if not isinstance(other,MyDate):
            return false
        return self.year ==other.year and self.month == other.month and self.day == other.day
    def __hash__(self):
        print("hash is called")
        return hash(self.year + self.month * 101 + self.day * 101)

def main():
    my_date_1 = MyDate(2011,11,3)
    my_date_2 = MyDate(2022, 11, 3)
    my_date_5 = MyDate(2020, 1, 1)

    my_date_3 = my_date_1





    print(my_date_1) #自动调用__str__
    my_date = MyDate(2024,11,9)
    print(repr(my_date))
    print(my_date_1 is my_date_3)
    print(my_date_1 == my_date_3)
    date_set = set()
    date_set.add(my_date_1)
    print(hash(my_date_1))



if __name__  == '__main__':
    main()