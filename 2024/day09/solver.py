import sys

# this is the formula for the sum of the first x natural numbers
# we can use this to calculate the sum within an interval [x, y]
# by subtracting the sum of the first x - 1 natural numbers from the sum of the first y natural numbers
# checksum(y) - checksum(x - 1) = (1 + 2 + ... + y) - (1 + 2 + ... + x - 1) = x + x + 1 + ... + y
checksum = lambda x: (x * (x + 1)) // 2

class Solver:
    def __init__(self, file_path = "test.txt"):
        # read input file
        with open(file_path) as f:
            self.lines = f.readlines()

        # parsing goes here
        self.data = list(map(int, self.lines[0].strip()))
        self.N = len(self.data)

    def part1(self):
        # this came out a bit confusing, there might be a less convoluted way to do this
        # basic idea is to iterate through the list and calculate the checksum for each block
        # and at each free block, try to fill it with the blocks from the end of the list
        total = 0
        
        i = 0
        j = self.N - 1 if self.N % 2 != 0 else self.N - 2
        pos = 0
        while i < self.N and i <= j:
            i_block = self.data[i]
            if i % 2 == 0:
                # non-free block
                id = i // 2
                last_pos = pos - 1
                pos += i_block

                total += id * (checksum(pos - 1) - checksum(last_pos))
            else:
                # free block
                while j > i and i_block > 0:
                    j_block = self.data[j]

                    # find how much of the last block we can move
                    moved_block = min(i_block, j_block)
                    
                    # calculate the checksum for the moved block
                    id = j // 2
                    last_pos = pos - 1
                    pos += moved_block

                    total += id * (checksum(pos - 1) - checksum(last_pos))

                    # update the free block space and the block we moved
                    i_block -= moved_block
                    self.data[j] -= moved_block
                    if j_block == 0:
                        j -= 2

            i += 1

        return total

    def part2(self):
        # this came out a bit simpler since the blocks are moved as a whole
        # we don't need to count how much has been moved, so we can just go by block (starting from the end)
        # and try to move it as much to the start as we can
        # and then calculate the checksum for the moved block
        total = 0

        # this initializes the position of each block based on the previous block sizes
        pos = [0] * self.N
        pos_counter = 0
        for i in range(self.N):
            pos[i] = pos_counter
            pos_counter += self.data[i]
        
        j = self.N - 1 if self.N % 2 != 0 else self.N - 2
        while j >= 0:
            j_block = self.data[j]
            id = j // 2

            i = 1
            moved = False
            while i <= j:
                i_block = self.data[i]
                if j_block <= i_block:
                    # we can move the whole block
                    last_pos = pos[i] - 1
                    n = pos[i] + j_block - 1
                    total += id * (checksum(n) - checksum(last_pos))

                    # update the position of the free space within the (originally) free block
                    pos[i] += j_block

                    # remove the size of that block from the free block space
                    self.data[i] -= j_block

                    moved = True
                    break
                i += 2

            if not moved:
                # is the block is too big to fit in any free space, we can just count it in its original position
                last_pos = pos[j] - 1
                n = pos[j] + j_block - 1
                total += id * (checksum(n) - checksum(last_pos))
            j -= 2

        return total
    
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