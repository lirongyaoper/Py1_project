from fontTools.misc.symfont import printGreenPen

cars = ['bmw','audi','toyota','subaru']
cars.sort()
print(cars)
# sort() 方法能永久地修改列表元素的排列顺序。现在，汽车是按字母顺序排列的，再也无法恢复到原来的排列顺序:
#['audi', 'bmw', 'subaru', 'toyota']
cars1 = ['bmw', 'audi', 'toyota', 'subaru']
cars1.sort(reverse=True)
print(cars1)
print("*********************************************************************")
cars2 = ['bmw', 'audi', 'toyota', 'subaru']
print("Here is the original list:")
print(cars2)
print("\nHere is the sorted list:")
print(sorted(cars2))
print("\nHere is the original list:")
print(cars2)

print("****************************反向打印列表*****************************************")
cars3 = ['bmw', 'audi', 'toyota', 'subaru']
print(cars3)
cars3.reverse()
print(cars3)
print("****************************确认列表的长度*****************************************")
cars4 = ['bmw', 'audi', 'toyota', 'subaru']
len_cars=len(cars4)
print(len_cars)
