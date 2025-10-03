

for value in range(1,5):
    print(value)
print("******************使用 range() 函数时，还可指定步长*************************")
for value1 in range(1,100,2):
    print(value1)
print("*************************使用 range() 创建数值列表************************")

numbers = list(range(1,6))
print(numbers)

print("*************************使用 range() 创建数值列表************************")
squares  = []
for value in range(1,11):
    square = value**2
    squares.append(square)
#    squares.append(value**2)
print(squares)

print("*************************对数值列表执行简单的统计计算***********************")
digits = list(range(1,13))
print(min(digits))
print(max(digits))
print(sum(digits))

print("****************************列表推导式**********************************")
"""
列表推导式（list comprehension）将 for 循环和创建新元素的代码合并成一行，并自动追加新元素。
面向初学者的书并非都会介绍列表推导式，这里之所以介绍，是因为你可能会在他人编写的代码中遇到列表推导式。
"""

squares1 =[value**2 for value in range(1,11)]
print(squares1)


print("****************************复制列表**********************************")
my_foods = ['pizza', 'falafel', 'carrot cake']
friend_foods = my_foods[:]

print("My favorite foods are:")
print(my_foods)

print("\nMy friend's favorite foods are:")
print(friend_foods)


print("****************************************************************")
my_foods1 = ['pizza', 'falafel', 'carrot cake']
friend_foods1 = my_foods1[:]
my_foods1.append('cannoli')
friend_foods1.append('ice cream')
print("My favorite foods are:")
print(my_foods1)

print("\nMy friend's favorite foods are:")
print(friend_foods1)
print("****************************************************************")
my_foods = ['pizza', 'falafel', 'carrot cake']
friend_foods = my_foods

my_foods.append('cannoli')
friend_foods.append('ice cream')

print("My favorite foods are:")
print(my_foods)

print("\nMy friend's favorite foods are:")
print(friend_foods)