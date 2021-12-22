# Part 1

from math import ceil, floor
import re

# Data Structure to represent Binary Tree
class Pair:
	def __init__(self, previous):
		self.left = None
		self.right = None
		self.data = None
		self.previous = previous
	def treeString(self):
		ignore = "_"
		if self.data != None:
			return f"{self.data}"
		else:
			return f"[{self.left.treeString() if self.left != None else ignore},{self.right.treeString() if self.right != None else ignore}]"

# Create new Binary Tree node with regular number
def newNumber(value, previous):
	number = Pair(previous)
	number.data = value
	return number

# Create new Binary Tree node with pair
def newPair(left, right, previous):
	pair = Pair(previous)
	pair.left = left
	pair.right = right
	return pair


# Calculates the split at the selected pair
def split(pair):
	number = pair.data
	pair.data = None
	pair.left = newNumber(floor(number/2), pair)
	pair.right = newNumber(ceil(number/2), pair)

# Calculate the explosion part where you add to the left
def explode_left(pair, origin, number):
	temp = pair
	if temp == None:
		return
	while temp.left == origin:
		origin = temp
		temp = temp.previous
		if temp == None:
			return

	temp = temp.left
	while temp.data == None:
		temp = temp.right

	temp.data += number

# Calculate the explosion part where you add to the right
def explode_right(pair, origin, number):
	temp = pair
	if temp == None:
		return
	while temp.right == origin:
		origin = temp
		temp = temp.previous
		if temp == None:
			return
	
	temp = temp.right
	while temp.data == None:
		temp = temp.left
	
	temp.data += number


# Calculates the explosion of the selected pair
def explode(pair):
	left_number = pair.left.data
	right_number = pair.right.data
	pair.data = 0
	pair.left = None
	pair.right = None
	temp = pair.previous
	explode_left(temp, pair, left_number)
	explode_right(temp, pair, right_number)
	

# pair: Binary Tree that represents current pair
# height: Height of current Binary Tree (equal to number of tymes it's been nested)
def reduction(pair, height):
	if pair == None:
		return True
	elif pair.data != None:
		if pair.data >= 10:
			split(pair)
			return False
		else:
			return "number"
	elif height == 4:
		explode(pair)
		return False
	else:
		left = reduction(pair.left, height + 1)
		if left or left == "number":
			if not reduction(pair.right, height + 1):
				return False
		else:
			return False

	return True

# p1, p2: pairs to add (represented in Binary Trees)
def addition(p1, p2):
	pair = newPair(p1, p2, None)
	p1.previous = pair
	p2.previous = pair
	done = False
	while not done:
		done = reduction(pair, 0)
		print(pair.treeString())
	return pair

# parse input string to Binary Tree
def parse(string, previous):
	node = None
	if len(string) >= 5:
		pattern = re.search(r'\[(\d|\[.*\]),(\d|\[.*\])\]$', string)
		groups = pattern.groups()
		print(string)
		print(groups)
		node = newPair(None, None, previous)
		node.left = parse(groups[0], node)
		node.right = parse(groups[1], node)
	else:
		node = newNumber(int(string), previous)
	return node

'''
teste1 = "[[[[4,3],4],4],[7,[[8,4],9]]]"
teste2 = "[1,1]"
n1 = parse(teste1, None)
n2 = parse(teste2, None)
print(n1.treeString())
print(n2.treeString())
n = addition(n1, n2)
#print(n.treeString())'''

file = open("teste2", 'r')

lines = file.readlines()

n = None

for i, line in enumerate(lines):
	if i == 0:
		n = parse(line[:-1], None)
	else:
		n2 = parse(line[:-1], None)
		n = addition(n, n2)
	print(n.treeString())