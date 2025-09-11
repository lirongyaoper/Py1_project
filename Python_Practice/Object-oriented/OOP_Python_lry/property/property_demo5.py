def A(x):
    print(x)
    def B(aa,bbb):
        print("B")
        print(aa,bbb)
        return x(aa,bbb)
    return B


@A
def C(n ,nn):
    print("C")

C("10","20")