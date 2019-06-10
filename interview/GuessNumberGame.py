'''
Created on 2017-04-01
@author: weipengzheng
'''
import random

def main():
    # Initialize the program
    print ("Guess a number between 1 and 100.")
    randomNumber = random.randint(1, 100)
    found = False
    # Run through the guessing process
    while not found:
        try:
            userGuess = int(input("Please enter a number as your guess: "))
        except ValueError:
            print("Oops! That was not a valid number. Try again...")
        if userGuess < randomNumber:
            print("Guess higher!")
        elif userGuess > randomNumber:
            print("Guess lower!")
        elif userGuess == randomNumber:
            print("You got it!")
            found = True
# main()
if __name__ == "__main__":
    main()
