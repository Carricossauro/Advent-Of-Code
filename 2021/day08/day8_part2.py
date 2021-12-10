# Part 2

def ocurrences(section, lista):
	total = 0
	for p in lista:
		if section in p:
			total += 1
	return total

def solve(line):
	code = {}
	numbers = {}
	lista = line.split('|')
	digits = lista[0].split()
	print(digits)
	for digit in digits:
		if len(digit) == 7: # digit = 8
			numbers[8] = set(digit)
		elif len(digit) == 3: # digit = 7
			numbers[7] = set(digit)
		elif len(digit) == 4: # digit = 4
			numbers[4] = set(digit)
		elif len(digit) == 2: # digit = 1
			numbers[1] = set(digit)

	for p in numbers[7]:
		print(p, numbers[7])
		if p not in numbers[1]:
			code['a'] = p
			break

	ocurrence_scheme = {6:'b', 4:'e', 9:'f'}
	for p in ['a','b','c','d','e','f','g']:
		oc = ocurrences(p, digits)
		if oc in ocurrence_scheme:
			code[ocurrence_scheme[oc]] = p
		if oc == 8 and p != code['a']:
			code['c'] = p
		elif oc == 7 and p in numbers[4]:
			code['d'] = p
		elif oc == 7:
			code['g'] = p

	# number 1
	numbers[1] = set(str(code['c'] + code['f']))
	# number 2
	numbers[2] = set(str(code['a'] + code['c'] + code['d'] + code['e'] + code['g']))
	# number 3
	numbers[3] = set(str(code['a'] + code['c'] + code['d'] + code['f'] + code['g']))
	# number 5
	numbers[5] = set(str(code['a'] + code['b'] + code['d'] + code['f'] + code['g']))
	# number 6
	numbers[6] = set(str(code['a'] + code['b'] + code['d'] + code['e'] + code['f'] + code['g']))
	# number 9
	numbers[9] = set(str(code['a'] + code['b'] + code['c'] + code['d'] + code['f'] + code['g']))
	# number 0
	numbers[0] = set(str(code['a'] + code['b'] + code['c'] + code['e'] + code['f'] + code['g']))

	n = ""
	digs = lista[1].split()
	for dig in digs:
		for p in range(0,10):
			if set(dig) == numbers[p]:
				n += str(p)
	print(n)
	return n

file = open("day8_part1.txt",'r')

lines = file.readlines()

lista = []
for line in lines:
	lista.append(solve(line[:-1]))

print(sum(map(int, lista)))