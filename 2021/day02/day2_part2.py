# Part 2

position = [0,0,0]

file = open("day2.txt", 'r')

for line in file.readlines():
	lista = line.split()
	if lista[0] == 'up':
		position[2] -= int(lista[1])
	elif lista[0] == 'down':
		position[2] += int(lista[1])
	elif lista[0] == 'forward':
		position[0] += int(lista[1])
		position[1] += position[2]*int(lista[1])
	
print(position[0] * position[1])