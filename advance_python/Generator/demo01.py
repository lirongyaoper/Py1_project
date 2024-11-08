def hello():   #a Iterators object
    print("step1")
    yield 1
    print("step 2")
    yield 2
    print("step 3")
    yield 3
    print("step 4")
    yield 4

g= hello()
# print(next(g))
# print(next(g))
# print(next(g))
# print(next(g))

for res in g:
    print(res)