# how do I get a sequence of numbers that doesn't start at 0?
print('What number should I start at?')
num1 = int(input())
print('What number should I end at (including this num)?')
num2 = int(input())
b = 1
for i in range(num1, num2 + 1):
    b *= i
print('The sum of all the numbers from ' + str(num1) + ' to ' + str(num2) + ' is ' + str(b))
# print(i)
# print('The sum of all the numbers from ' + str(10) + ' to ' + str(20) + ' is ' + str(145))
