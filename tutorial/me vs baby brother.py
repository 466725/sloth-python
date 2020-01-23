andySpeed = int(input('Choose Andys speed'))
babyBrotherSpeed = int(input('Choose babys speed'))
if babyBrotherSpeed > andySpeed:
    print('Andy could never catch his brother')
print('Andy sprints at a speed of ' , str(andySpeed) , ' km per minute and his baby brother craws at a speed of ' , str(babyBrotherSpeed) , ' km per minute.')
print(' ')
print('Andy is chasing his brother but his brother got a head start.')
print(' ')
cheating = int(input('You get to choose how many minutes ago his brother started:'))
print(' ')
AndyPlace = 0
BrotherPlace = cheating * babyBrotherSpeed
AndyPlace += andySpeed
BrotherPlace += babyBrotherSpeed
#
a = andySpeed - babyBrotherSpeed
b = cheating * babyBrotherSpeed // a
print('It took Andy ' + str(b) + ' minutes to catch his brother.')
print(' ')
print(' ')
print(' ')
print(' ')