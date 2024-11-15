class Vehicle():
    can_fly = False
    number_of_weels = 0


class Car(Vehicle):
    number_of_weels = 4

    def __init__(self, color):
        self.color = color


my_car = Car("red")
print(my_car.__dict__['color'])
print(type(my_car).__dict__['number_of_weels'])
print(type(my_car).__base__.__dict__['can_fly'])
print(type(my_car).__dict__)
print(type(my_car).__base__.__dict__)

"""
那么，当您使用点符号访问对象的属性时会发生什么？Python 解释器是如何知道您的真正需求？好吧，这里有一个叫做查找链的概念：
首先，您将从以所要查找的属性命名的数据描述符__get__方法返回结果。
如果失败，那么您将获得实例对象的__dict__值，该值是根据要查找的属性命名的键。
如果失败，那么将从以您要查找的属性命名的非数据描述符__get__方法中返回结果。
如果失败，那么您将获得类型对象的__dict__值，该值是根据要查找的属性命名的键。
如果失败，那么您将获得父类的__dict__值，该值是根据要查找的属性命名的键。
如果失败，那么将按照对象的方法解析顺序对所有父类重复上一步。
如果其他所有操作均失败，则将出现AttributeError异常。


现在，您明白为什么要知道描述符是数据描述符还是非数据描述符是如此重要了吧？它们位于查找链的不同层次上，稍后您会发现这种行为上的差异非常方便。
"""
"""
译者注：同时定义了 __get__ 和 __set__的描述符称为 数据描述符(data descriptor)；仅定义了 __get__ 的称为 非数据描述符(non-data descriptor) 。
两者区别在于：如果 obj.__dict__ 中有与描述符同名的属性，若描述符是数据描述符，则优先调用描述符，若是非数据描述符，则优先使用 obj.__dict__ 中属性。
通过类型对象的__dict__属性访问,通过父类对象的__dict__属性访问。

"""