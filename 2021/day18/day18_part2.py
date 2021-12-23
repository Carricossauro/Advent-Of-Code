# Part 2

from math import ceil, floor
import re
from typing import NewType
from pyparsing import nestedExpr


# Data Structure to represent Binary Tree
class Pair:
    def __init__(self, previous):
        self.left = None
        self.right = None
        self.data = None
        self.previous = previous

    def __str__(self):
        return self.treeString()

    def treeString(self):
        ignore = "_"
        if self.data != None:
            return f"{self.data}"
        else:
            return f"[{self.left.treeString() if self.left != None else ignore},{self.right.treeString() if self.right != None else ignore}]"

    def magnitude(self):
        if self.data == None:
            return 3 * self.left.magnitude() + self.right.magnitude() * 2
        else:
            return self.data
    
    def clone(self):
        newPair = Pair(None)
        if self.data != None:
            newPair.data = self.data
        else:
            newPair.left = self.left.clone()
            newPair.right = self.right.clone()
            newPair.left.previous = newPair
            newPair.right.previous = newPair
        return newPair

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
	
def explosion(pair, height):
	if pair.data == None:
		if height == 4:
			explode(pair)
			return True
		else:
			left = explosion(pair.left, height + 1)
			right = False if left else explosion(pair.right, height + 1)
			if left or right:
				return True
	else:
		return False
	return False

def splits(pair):
	if pair.data != None:
		if pair.data >= 10:
			split(pair)
			return True
	else:
		left = splits(pair.left)
		right = False if left else splits(pair.right)
		if left or right:
			return True
	return False

# p1, p2: pairs to add (represented in Binary Trees)
def addition(p1, p2):
	pair = newPair(p1, p2, None)
	p1.previous = pair
	p2.previous = pair
	while True:
		exploded = explosion(pair, 0)
		if exploded:
			continue
		splitted = splits(pair)
		if not splitted:
			break
	return pair

# parse input string to Binary Tree
def parse(nested_list, previous):
	node = None
	if not isinstance(nested_list, str):
		node = newPair(None, None, previous)
		node.left = parse(nested_list[0], node)
		node.right = parse(nested_list[1], node)
	else:
		node = newNumber(int(nested_list), previous)
	return node

file = open("day18.txt", 'r')

lines = file.readlines()

n = None

nested_braces = nestedExpr('[', ']')

pairs = []

for i, line in enumerate(lines):
    nested_list = nested_braces.parseString(line.replace(',', ' ')).asList()[0]
    n = parse(nested_list, None)
    pairs.append(n)

magnitudes = []

for i, p1 in enumerate(pairs):
    for j, p2 in enumerate(pairs):
        if i != j:
            pair = addition(p1.clone(), p2.clone())
            magnitudes.append(pair.magnitude())
            print("p1", p1)
            print("p2", p2)
            print("result", pair)
            print("magnitude", magnitudes[-1])

print(max(magnitudes))