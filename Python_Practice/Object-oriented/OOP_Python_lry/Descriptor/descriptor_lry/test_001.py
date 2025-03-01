class Test(object):
    cls_val =  1
    def __init__(self):
        self.ins_val = 2

t = Test()
print("****************************************************************")
print(Test.__dict__)
print("\n")
print(t.__dict__)
print("****************************************************************")
t.cls_val = 20
print(Test.__dict__)
print("\n")
print(t.__dict__)
print("****************************************************************")
Test.cls_val = 10
print(Test.__dict__)
print("\n")
print(t.__dict__)