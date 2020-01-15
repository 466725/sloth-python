#Create inputs that ask for the team names
teamA = str(input('What is the first teams name? :'))
teamB = str(input('What is the second teams name? :'))
#Create inputs that ask for the score
score1 = int(input('What is the first teams score? :'))
score2 = int(input('What is the second teams score? :'))
#Print the winning teams name.
if score1 > score2:
  print(teamA , 'beat' , teamB)
elif score2 > score1:
  print(teamB , 'beat' , teamA)





