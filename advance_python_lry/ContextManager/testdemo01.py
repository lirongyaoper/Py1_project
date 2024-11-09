import time

start = time.perf_counter()
nums = []
for n in range(10000):
    nums.append(n **2)
stop = time.perf_counter()
elapsed = stop - start
print(elapsed)