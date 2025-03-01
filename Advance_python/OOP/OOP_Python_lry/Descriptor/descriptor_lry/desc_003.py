class A (object):
    name = "unchange"
    def __init__(self,value):
        print ("into A __init__")
        self.value = value

    def __get__(self, instance, owner):
        print ("into __get__")
        print(instance ,owner)


class B(object):
    value = A(10)
    def __init__(self, value):
        print("into B __init__")



b = B(20)
print('='*40,'\n')
print (b.value)