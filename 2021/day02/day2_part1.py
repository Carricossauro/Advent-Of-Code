# Part 1

position = [0,0]

file = open("day2.txt",'r')

moves = {'up':(0,-1), 'down':(0,1), 'forward':(1,0)}

for line in file.readlines():
	lista = line.split()
	position[0] += moves[lista[0]][0] * int(lista[1])
	position[1] += moves[lista[0]][1] * int(lista[1])

print(position[0] * position[1])