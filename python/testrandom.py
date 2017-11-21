'''
Final distribution: [10300, 10069, 10186, 10341, 10128, 10161, 9554, 9776, 9810, 9675]
Runtime for 100000 numbers was 148 seconds
Final distribution: [10235, 10014, 10099, 10182, 9779, 9861, 9830]
Runtime for 70000 numbers was 98 seconds
Final distribution: [9975, 10025]
Runtime for 20000 numbers was 27 seconds
'''
from cockle import randint
from time import time
start = time()
bound = 2
count = 0
target = bound * 10000
l = [0 for i in range(bound)]
while count < target:
    l[randint(0, bound)] += 1
    if count & 1023 == 1023:
        print(l)
    count += 1
end = time()
print("Final distribution: {}".format(l))
print("Runtime for {} numbers was {} seconds".format(target, end - start))
