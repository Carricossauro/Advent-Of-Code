from functools import reduce
import re

def solve():
    with open('day02/input2.txt') as f:
        lines = f.readlines()

    total = 0
    for line in lines:
        minimum = {
            'red': 0,
            'green': 0,
            'blue': 0,
        }
        
        set = re.findall(r"(\d+ \w+)", line)
        for ballz in set:
            [number, color] = ballz.split(' ')
            minimum[color] = max(minimum[color], int(number))

        total += reduce(lambda x, y: x * y, minimum.values())

    return total

if __name__ == '__main__':
    print(solve())