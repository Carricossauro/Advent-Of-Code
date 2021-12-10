# Part 1

total = 0

def solve(line,total):
	lista = line.split('|')
	digits = lista[1].split()
	print(digits)
	for digit in digits:
		if len(digit) == 7: # digit = 8
			total += 1
		elif len(digit) == 3: # digit = 7
			total += 1
		elif len(digit) == 4: # digit = 4
			total += 1
		elif len(digit) == 2: # digit = 1
			total += 1
	return total

file = open("day8.txt",'r')

lines = file.readlines()

for line in lines:
	total = solve(line[:-1], total)

print(total)