def A(x):
    def B():
        print("B")
        return x
    return B()


@A
def C():
    print("C")

C()