def A(x):
    def B():
        print("B")
    B()
    return x
@A
def C():
    print("c")

C()