# Part 1

file = open("day6.txt",'r')

fishes = list(map(int, file.readline()[:-1].split(',')))

print(fishes)

for day in range(80):
	new = []
	for i, p in enumerate(fishes):
		if p == 0:
			new.append(8)
			fishes[i] = 6
		else:
			fishes[i] = p - 1
	fishes += new
	# print(day+1, fishes)

print(len(fishes))