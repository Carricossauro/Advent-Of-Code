# Part 1

file = open("day10_part1.txt",'r')

lines = file.readlines()

error = 0
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
				error += value[c]
				print(c, value[c])
				break
			else:
				chunks.pop()

print(error)