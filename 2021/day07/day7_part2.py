# Part 2

file = open("day7.txt", 'r')

lista = list(map(int, file.readline().split(',')))
print(lista)

N = max(lista)
print(f"N = {N}")

dic = {}

for i in range(N):
	dic[i] = 0
	for p in lista:
		dic[i] += sum([n for n in range(1, abs(i-p)+1)])

print(dic)

minimum = min(dic.values())

print(f"Min = {minimum}")