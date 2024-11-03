
print("###################### 修改列表元素####################################")
motorcycles = ['honda','yamaha','suzuki']
print(motorcycles)
# 修改列表元素
motorcycles[0]="ducati"
print(motorcycles)
print("###################### 添加列表元素####################################")
# 添加列表元素
motorcycles.append('feige')
print(motorcycles)
motorcycles1 = []
motorcycles1.append('hondda')
motorcycles1.append('yamaha')
motorcycles1.append('suzuku')
print(motorcycles1)
print("#####################列表插入元素####################################")

# 列表插入元素
motorcycles2 = ['honda','yamaha','suzuki']
motorcycles2.insert(0,'ducati')
print(motorcycles2)
print("#####################删除列表中的元素####################################")
# 删除列表中的元素
motorcycles3 =['honda','yamaha','suzuki']
print(motorcycles3)
del motorcycles3[0]
print(motorcycles3)
#使用 del 可删除任意位置的列表元素，只需要知道其索引即可。使用 del 语句将值从列表中删除后，你就无法再访问它了。

print("#####################POP删除列表中的元素####################################")
motorcycles4 = ['honda','yamaha','suzuki']
print(motorcycles4)
popped_motorcycle= motorcycles4.pop()
print(motorcycles4)
print(popped_motorcycle)
#实际上，也可以使用 pop() 删除列表中任意位置的元素，只需要在括号中指定要删除的元素的索引即可。
motorcycles5 = ['honda','yamaha','suzuki']
first_owned = motorcycles5.pop(0)
print(f"the first motorcycle I owned was a {first_owned.title()}.")

print("#####################remove删除列表中的元素####################################")

motorcycles6 = ['honda', 'yamaha', 'suzuki', 'ducati']
print(motorcycles6)

motorcycles6.remove('ducati')
print(motorcycles6)

print("#####################remove删除列表中的元素####################################")

# 使用 remove() 从列表中删除元素后，也可继续使用它的值
