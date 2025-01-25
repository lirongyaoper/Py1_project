# lookup.py
class Vehicle(object):
    can_fly = False
    number_of_weels = 0

class Car(Vehicle):
    number_of_weels = 4

    def __init__(self, color):
        self.color = color

my_car = Car("red")

print(my_car.color)
print(my_car.number_of_weels)
print(my_car.can_fly)
print("*"*40,"\n")
print(my_car.__dict__)
print(type(my_car).__dict__)
