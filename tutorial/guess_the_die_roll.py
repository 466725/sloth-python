import random

num = random.randint(1, 6)
# print(num)
guess = int(input('Guess what the die rolled:'))


# function (what do you return?)
def dieRoll():
    if num == guess:
        print('You guessed correctly!!!')
        return True
    else:
        print('Nope. ')
        return False


# how do you replay the game multiple times?
dieRoll()
if guess != num:
    for i in range(2):
        guess = int(input('Guess again:'))
        # num = random.randint(1,6)
        dieRoll()
    print('It was', str(num))
