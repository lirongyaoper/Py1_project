func_list = []
for i in range (3):
    def myfunc(a):
        return i +a
    func_list.append(myfunc)
for f in func_list:
    print(f(1))
