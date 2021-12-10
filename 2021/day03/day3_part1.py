# Part 1

gamma_binary = ""
epsilon_binary = ""
lines = []

file = open("day3.txt", 'r')

lines = file.readlines()

for pos in range(len(lines[0])-1):
	freq = [0,0]
	for line in lines:
		freq[int(line[pos])] += 1
	if freq[0] > freq[1]:
		gamma_binary += "0"
		epsilon_binary += "1"
	else:
		gamma_binary += "1"
		epsilon_binary += "0"

	print(freq, gamma_binary, epsilon_binary)

print("gb - ", gamma_binary)
print("eb - ", epsilon_binary)


gamma_binary = gamma_binary[::-1]
epsilon_binary = epsilon_binary[::-1]
gamma_soma = 0
epsilon_soma = 0
exp = 0

for p in range(len(gamma_binary)):
	gamma_soma += int(gamma_binary[p]) * 2**exp
	epsilon_soma += int(epsilon_binary[p]) * 2**exp
	exp += 1

print(gamma_soma)
print(epsilon_soma)
print(gamma_soma * epsilon_soma)