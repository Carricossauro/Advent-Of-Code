import sys

# this is literally just creating a hashmap lol
# Algoritmos e Complexidade type shit
class Solver:
    def __init__(self, file_path = "test.txt"):
        # read input file
        with open(file_path) as f:
            self.lines = f.readlines()

        self.strings = self.lines[0].strip().split(',')

    # hash a string to a number between 0 and 255
    def hash(self, string):
        num = 0

        for char in string:
            num = ((num + ord(char)) * 17) % 256

        return num

    def part1(self):
        total = 0

        for string in self.strings:
            total += self.hash(string)

        return total

    # requires self.hashmap to be initialized
    # add a lens with the given label and focal length
    def place_lens(self, label, focal_length):
        for i, (l, f) in enumerate(self.hashmap[self.hash(label)]):
            if l == label:
                self.hashmap[self.hash(label)][i] = (label, focal_length)
                return None

        self.hashmap[self.hash(label)].append((label, focal_length))
    
    # requires self.hashmap to be initialized
    # remove the first lens with the given label
    def remove_lens(self, label):
        for i, (l,f) in enumerate(self.hashmap[self.hash(label)]):
            if l == label:
                self.hashmap[self.hash(label)].pop(i)

    def part2(self):
        self.hashmap = [[] for _ in range(256)]

        for i, string in enumerate(self.strings):
            if string[-1] == '-':
                # remove the lens
                self.remove_lens(string[:-1])
            else:
                # add/change the lens
                label, focal_length = string.split('=')
                self.place_lens(label, int(focal_length))

        focusing_power = 0
        # iterate through the boxes and add any lens still in the hashmap
        for i, box in enumerate(self.hashmap):
            for j, (label, focal_length) in enumerate(box):
                focusing_power += (i + 1) * (j + 1) * focal_length

        return focusing_power
    
if __name__ == '__main__':
    if len(sys.argv) > 2 and 1 <= int(sys.argv[1]) <= 2:

        if sys.argv[2] == 'test':
            solver = Solver("test.txt")
        elif sys.argv[2] == 'test2':
            solver = Solver("test2.txt")
        elif sys.argv[2] == '1':
            solver = Solver("input1.txt")
        elif sys.argv[2] == '2':
            solver = Solver("input2.txt")

        if sys.argv[1] == '1':
            print(solver.part1())
        else:
            print(solver.part2())
    else:
        print("Usage: python3 solver.py [1 / 2] [test / test2 / 1 / 2]")
        print("Filenames: test.txt\n\t   test2.txt\n\t   input1.txt\n\t   input2.txt")