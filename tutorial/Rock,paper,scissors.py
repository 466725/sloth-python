#Things you may need.
Q1 = str(input('Do you wish to play agianst a mcu or another player'))
if Q1 == 'mcu':
	user = str(input('choose beetween rock paper and scissers:'))
	import random
	Thislist = ['scissers','rock','paper']
	a = random.randint(0,3)
	mcu = Thislist[a]
	if mcu == user:
		print(user , '!!!')
		print(mcu , '!!!')
		print('You tied!!!')
	elif mcu == 'scissers' and user == 'rock':
		print(user , '!!!')
		print(mcu , '!!!')
		print('You won!!!')
	elif mcu == 'rock' and user == 'paper':
		print(user , '!!!')
		print(mcu , '!!!')
		print('You won!!!')
	elif mcu == 'paper' and user == 'scissers':
		print(user , '!!!')
		print(mcu , '!!!')
		print('You won!!!')
	elif mcu == 'rock' and user == 'scissers':
		print(user , '!!!')
		print(mcu , '!!!')
		print('You lost!!!')
	elif mcu == 'scissers' and user == 'paper':
		print(user , '!!!')
		print(mcu , '!!!')
		print('You lost!!!')
	elif mcu == 'paper' and user == 'rock':
		print(user , '!!!')
		print(mcu , '!!!')
		print('You lost!!!')
	#You should know how to use import
	#You should know how to use input
	#You should know how to use booleans
	#You should understand conditionas
	#You should know how to use print
	#You should know how to use loops
	#You should know how to use return
elif Q1 == 'another player':
	user1 = str(input('choose beetween rock paper and scissers:'))
	user2 = str(input('choose beetween rock paper and scissers( you too ):'))
	if user1 == user2:
		print(user1 , '!!!')
		print(user2 , '!!!')
		print('You two tied!!!')
	elif user1 == 'scissers' and user2 == 'rock':
		print(user1 , '!!!')
		print(user2 , '!!!')
		print('User2 won!!!')
	elif user1 == 'rock' and user2 == 'paper':
		print(user1 , '!!!')
		print(user2 , '!!!')
		print('User2 won!!!')
	elif user1 == 'paper' and user2 == 'scissers':
		print(user1 , '!!!')
		print(user2 , '!!!')
		print('User2 won!!!')
	elif user1 == 'rock' and user2 == 'scissers':
		print(user1 , '!!!')
		print(user2 , '!!!')
		print('User1 won!!!')
	elif user1 == 'scissers' and user2 == 'paper':
		print(user1 , '!!!')
		print(user2 , '!!!')
		print('User1 won!!!')
	elif user1 == 'paper' and user2 == 'rock':
		print(user1 , '!!!')
		print(user2 , '!!!')
		print('User1 won!!!')