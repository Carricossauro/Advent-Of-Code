# Part 2

file = open("day10_part1.txt",'r')

lines = file.readlines()

total = []
for line in lines:
	chunks = []

	for c in line:
		if c == '\n':
			break
		if c in ['(', '{', '[', '<']:
			chunks.append(c)
		else:
			value = {')':3, ']':57, '}':1197, '>':25137}
			if len(chunks) == 0 or (chunks[-1] != '(' and c == ')') or (chunks[-1] != '[' and c == ']') or (chunks[-1] != '<' and c == '>') or (chunks[-1] != '{' and c == '}'):
				chunks = []
				break
			else:
				chunks.pop()
	error = 0
	if len(chunks) != 0:
		for p in chunks[::-1]:
			values = {'(': 1, '[':2, '{':3, '<':4}
			error = error *5 + values[p]
		total.append(error)
		print(error, total)

total.sort()
print(total[len(total)//2])