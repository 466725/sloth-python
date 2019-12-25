andySpeed = 3
babyBrotherSpeed = 2
print('Andy sprints at a speed of 3 km per minute and his baby brother craws at a speed of 2 km per minute.')
print(' ')
print('Andy is chasing his brother but his brother got a head start.')
print(' ')
cheating = int(input('You get to choose how many minutes ago his brother started:'))
print(' ')
AndyPlace = 0
BrotherPlace = cheating * 2
AndyPlace += andySpeed
BrotherPlace += babyBrotherSpeed
#
a = andySpeed - babyBrotherSpeed
b = cheating * 2 // a
print('It took Andy ' + str(b) + ' minutes to catch his brother.')
print(' ')
print(' ')
print(' ')
print(' ')
for i in range(100):
    andySpeed = 3
    babyBrotherSpeed = 2
    print('Andy sprints at a speed of 3 km per minute and his baby brother craws at a speed of 2 km per minute again.')
    print(' ')
    print('Andy is chasing his brother but his brother got a head start again.')
    print(' ')
    cheating = int(input('You get to choose how many minutes ago his brother started again:'))
    print(' ')
    AndyPlace = 0
    BrotherPlace = cheating * 2
    AndyPlace += andySpeed
    BrotherPlace += babyBrotherSpeed
    #
    a = andySpeed - babyBrotherSpeed
    b = cheating * 2 // a
    print('It took Andy ' + str(b) + ' minutes to catch his brother.')
    print(' ')
    print(' ')
    print(' ')
    print(' ')
