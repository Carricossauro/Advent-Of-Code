def solve():
    with open('day01/input1.txt') as f:
        lines = f.readlines()

    total = 0
    for line in lines:
        first = None
        last = None
        for character in line:
            if character.isdigit():
                if first is None:
                    first = int(character)
                last = int(character)

        total += (first*10)+last

    return total

if __name__ == '__main__':
    print(solve()) 