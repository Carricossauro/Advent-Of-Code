# Part 1

file = open("day7_part1.txt", 'r')

lista = list(map(int, file.readline().split(',')))
print(lista)

N = max(lista)
print(f"N = {N}")

dic = {}

for i in range(N):
	dic[i] = 0
	for p in lista:
		dic[i] += abs(i-p)

print(dic)

minimum = min(dic.values())

print(f"Min = {minimum}")