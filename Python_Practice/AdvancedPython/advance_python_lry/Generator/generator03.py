def squares(count:int):
    for n in range(count):
        yield n **2



squ_next = squares(4)
print(next(squ_next))
print(next(squ_next))
print(next(squ_next))
print(next(squ_next))

print("****************************************")
for sq in squares(4):
    print(sq)