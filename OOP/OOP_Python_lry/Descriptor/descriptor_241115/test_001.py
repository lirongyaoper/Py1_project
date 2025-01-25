class  Verbose_attribute():
    def __get__(self, instance, type=None) ->object:
        print("accessing the attribute to get the value")
        return 42
    def __set__(self, instance, value)->None:
        print("accessing the attribute to set the value")
        raise AttributeError("Cannot change the value")

class Foo():
    attribute1  = Verbose_attribute()
my_foo_object = Foo()
x = my_foo_object.attribute1
print(x)
