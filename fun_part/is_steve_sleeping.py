# How can you ask a user for information?
# How can you include if and else into a question
for x in range(6):
    print("Is Steve sleeping")
    steveSleeping = str(input())
    if steveSleeping == "yes":
        #        :(
        print("Steve woke up")
    elif steveSleeping == "no":
        #         :)
        print("Steve went to sleep")
    elif steveSleeping == "AHH":
        #        :(
        print("Steve woke up")
    else:
        #              :|
        print("Steve did not respond")
