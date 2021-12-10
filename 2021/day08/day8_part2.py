# Part 2

def solve(line):
	code = {}
	numbers = {}
	lista = line.split('|')
	digits = lista[0].split()
	print(digits)
	for digit in digits:
		if len(digit) == 7: # digit = 8
			numbers[8] = digit
		elif len(digit) == 3: # digit = 7
			numbers[7] = digit
		elif len(digit) == 4: # digit = 4
			numbers[4] = digit
		elif len(digit) == 2: # digit = 1
			numbers[1] = digit

	digits.remove(numbers[1])
	digits.remove(numbers[4])
	digits.remove(numbers[7])
	digits.remove(numbers[8])
	for p in numbers[7]:
		print(p, numbers[7])
		if p not in numbers[1]:
			code['a'] = p
			break
	print(digits)
	print(numbers)
	print(code)

file = open("teste",'r')

lines = file.readlines()

for line in lines:
	solve(line[:-1])
	break