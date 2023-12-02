import re

def solve():
    limit = {
        'red': 12,
        'green': 13,
        'blue': 14,
    }

    with open('day02/input1.txt') as f:
        lines = f.readlines()

    total = 0
    for line in lines:
        game_number = int(re.search(r"Game (\d+)", line).group(1))
        
        set = re.findall(r"(\d+ \w+)", line)
        possible = True
        for ballz in set:
            [number, color] = ballz.split(' ')
            if int(number) > limit[color]:
                possible = False
                break

        if possible:
            total += game_number

    return total

if __name__ == '__main__':
    print(solve())