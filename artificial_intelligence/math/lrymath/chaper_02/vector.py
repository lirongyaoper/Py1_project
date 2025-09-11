from math import  sin, cos ,pi
def to_cartesian(polar_vector):
    length,angle = polar_vector[0],polar_vector[1]
    return (length*cos(angle),length*sin(angle))
angle1 = 37*pi /180
tuple_1 = to_cartesian((10,angle1))
print(tuple_1)