"""
Created on 2017-04-01
@author: weipengzheng
"""

import random


def main():
    # Begin the program
    guess = 1
    print("Guess a number between 1 and 100.")
    random_number = random.randint(1, 100)
    found = False
    # Run through the guessing process
    while not found:
        try:
            guess = int(input("Please enter a number as your guess: "))
        except ValueError:
            print("Oops! That was not a valid number. Try again...")
        if guess < random_number:
            print("Guess higher!")
        elif guess > random_number:
            print("Guess lower!")
        elif guess == random_number:
            print("You got it!")
            found = True


# main()
if __name__ == "__main__":
    main()
