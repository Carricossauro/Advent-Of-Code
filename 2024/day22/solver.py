import sys

class Solver:
    def __init__(self, file_path = "test.txt"):
        # read input file
        with open(file_path) as f:
            self.lines = f.readlines()

        # parsing goes here
        self.numbers = []

        for line in self.lines:
            self.numbers.append(int(line.strip()))

        self.testing = file_path.startswith("test")

    def part1(self):
        # this day was simple, it doesn't require any optimization
        # it's a bit slow but it works
        for _ in range(2000):
            for i, number in enumerate(self.numbers):
                self.numbers[i] = self.evolve_number(number)

        return sum(self.numbers)

    def part2(self):
        # part 2 was just a matter of adding a bit of bookkeeping
        price_changes = [[] for _ in self.numbers]
        bananas = {}

        for k in range(2000):
            for i, number in enumerate(self.numbers):
                new_number = self.evolve_number(number)

                # register all the price changes
                # this could be optimized by just keeping the last 4 but there's no point in bothering
                old_ones = number % 10
                new_ones = new_number % 10
                price_changes[i].append(new_ones - old_ones)

                if k >= 3:
                    # if we have enough price changes, find the last 4 and add the bananas to its total
                    last_4 = tuple(price_changes[i][-4:])

                    if last_4 not in bananas:
                        bananas[last_4] = {'total': 0, 'monkeys': set()}

                    if i not in bananas[last_4]['monkeys']:
                        bananas[last_4]['total'] += new_number % 10
                        bananas[last_4]['monkeys'].add(i)

                self.numbers[i] = new_number

        return bananas[max(bananas, key=lambda x: bananas[x]['total'])] if self.testing else max([bananas[x]['total'] for x in bananas])
    
    def evolve_number(self, number):
        # this function does exactly what the instructions say
        # simple enough
        x = number * 64
        number = (number ^ x) % 16777216

        x = number // 32
        number = (number ^ x) % 16777216
        
        x = number * 2048
        number = (number ^ x) % 16777216

        return number
    
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