# create a counter to count how many correct answers
# create questions using input that check answers
# be creative with your questions like
# "Calculate the circumfrence of a parallelogram ... "
# "You can't"
counter = 0
q1 = (input('Calculate the circumfrence of a parallelogram ...'))
if q1 == 'you cant!!!':
    print('correct')
    counter += 1
    print('your score is', str(counter))
else:
    print('you are incorrect')
    print('your score is', str(counter))
q2 = (input('!?k.O sI noitseuQ sihT oT resnA ehT ,seY hO sdrawkcaB noitseuQ sihT resnA'))
if q2 == 'k.O':
    print('correct')
    counter += 1
    print('your score is', str(counter))
else:
    print('you are incorrect')
    print('your score is', str(counter))
q3 = (input('how did the frog jump higher then the CN tower?????????'))
if q2 == 'CN tower cant jump':
    print('correct')
    counter += 1
    print('your score is', str(counter))
else:
    print('you are incorrect')
    print('your score is', str(counter))
