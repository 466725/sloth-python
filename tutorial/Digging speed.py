personA = int(input('How many days does it take for person number 1 to finish digging( choose a number)?:'))
personB = int(input('How many days does it take for person number 2 to finish digging( choose a number)?:'))
personC = int(input('How many days does it take for person number 3 to finish digging( choose a number)?:'))
a = personA * personB + personB * personC + personA *  personC
b = personA * personB * personC
print('it takes ' + str(a) + '/' + str(b) + ' days')