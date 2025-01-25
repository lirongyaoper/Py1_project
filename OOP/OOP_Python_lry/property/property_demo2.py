def dec(a):
    print(a)
    print("修饰器函数")
    return a
@dec
def funA():
    print("被修饰函数")
funA()

print("东方大国")