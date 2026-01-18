'''
Created on 2017-04-01
@author: weipengzheng
'''

for num in range(1, 6):
    if num % 3 == 0 and num % 5 == 0:
        print(str(num) + ": Fizz + Buzz! ")
    elif num % 3 == 0:
        print(str(num) + ": Fizz.")
    elif num % 5 == 0:
        print(str(num) + ": Buzz. ")

# Fibonacci Sequence
a, b, = 0, 1
for i in range(1, 10):
    print("a: " + str(a) + "; b: " + str(b))
    a, b = b, a + b

# Fibonacci Sequence
a, b, c = 0, 1, 1
for i in range(1, 10):
    print("a: " + str(a) + "; b: " + str(b))
    c = a + b
    a = b
    b = c


# Fibonacci Generator
def fib(num):
    a, b = 0, 1
    for i in range(1, num + 1):
        yield "{}: {}".format(i, a)
        a, b = b, a + b


for item in fib(10):
    print(item)

my_list = [10, 20, 30, 40, 50, 60, 70, 80, 90]
for i in my_list:
    print(i)
squares = [num * num for num in my_list]
print(squares)

my_tuples = (1, 2, 3, 4, 5, 6, 7, 8, 9, 10)
for i in my_tuples:
    print(i)

my_dict = {'First Name': 'Weipeng', 'Last Name': 'Zheng', 'Cell Phone': '647-621-1311'}
print(my_dict.__sizeof__)
print(my_dict.items())
print(my_dict.keys())
print(my_dict.values())

my_set = [10, 20, 20, 20, 30, 40, 50, 60, 70, 80, 90]
for i in my_set:
    print(i)

# simple iteration
a = []
for x in range(10):
    a.append(x * 2)
print(a)

# list comprehension
a = [x * 2 for x in range(10)]
print(a)

# dict comprehension
a = {x: x * 2 for x in range(10)}
print(a)

# the basic way
s = 0
for x in range(10):
    s += x
print(s)

# the right way
s = sum(range(10))
print(s)


def f(x, l=[]):
    for i in range(x):
        l.append(i * i)
    print(l)


f(2)
f(3, [3, 2, 1])
f(3)


# Do you know what is the difference between lists and tuples? Can you give me an example for their usage?
# First list are mutable tuples not, tuples are used when the order of the elements in the sequence matters
# Do you know the difference between range and xrange?
# Range returns a list while xrange returns a generator xrange object which takes the same memory
# range removed in python 3
# Decorators allow you to inject or modify code in functions or classes
# Python is dynamically typed, You can do things like x=111 and then x="I'm a string" without error
# Monkey patching is changing the behaviour of a function or object after it has already been defined
# Use *args when we aren't sure how many arguments are going to be passed to a function
# **kwargs is used when we dont know how many keyword arguments will be passed to a function

def f(*args, **kwargs): print(args, kwargs)


l = [1, 2, 3]
t = (4, 5, 6)
d = {'a': 7, 'b': 8, 'c': 9}

f()
f(1, 2, 3)  # (1, 2, 3) {}
f(1, 2, 3, "groovy")  # (1, 2, 3, 'groovy') {}
f(a=1, b=2, c=3)  # () {'a': 1, 'c': 3, 'b': 2}
f(a=1, b=2, c=3, zzz="hi")  # () {'a': 1, 'c': 3, 'b': 2, 'zzz': 'hi'}
f(1, 2, 3, a=1, b=2, c=3)  # (1, 2, 3) {'a': 1, 'c': 3, 'b': 2}
f(*l, **d)  # (1, 2, 3) {'a': 7, 'c': 9, 'b': 8}
f(*t, **d)  # (4, 5, 6) {'a': 7, 'c': 9, 'b': 8}


def f1(lIn):
    l1 = sorted(lIn)
    l2 = [i for i in l1 if i < 0.5]
    return [i * i for i in l2]


def f2(lIn):
    l1 = [i for i in lIn if i < 0.5]
    l2 = sorted(l1)
    return [i * i for i in l2]


def f3(lIn):
    l1 = [i * i for i in lIn]
    l2 = sorted(l1)
    return [i for i in l1 if i < (0.5 * 0.5)]


import cProfile
import random

lIn = [random.random() for i in range(100000)]
cProfile.run('f1(lIn)')
cProfile.run('f2(lIn)')
cProfile.run('f3(lIn)')
