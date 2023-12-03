def solve():
    # read in the input
    with open('day03/input2.txt', 'r') as f:
        lines = f.readlines()

    # get the number of rows and columns
    N = len(lines)
    M = len(lines[0].strip())

    total = 0

    # store the numbers' and the possible gears' positions
    data = {
        'numbers': [],
        '*': []
    }
    for i, line in enumerate(lines):
        number = ''
        start = None # start position of number
        end = None # end position of number

        for j, char in enumerate(line):
            if char == '*':
                data['*'].append((i,j))
            if char.isdigit():
                # if the start position of the number has not been set, set it
                if not number:
                    start = (i,j)

                number += char
            elif number != '':
                # set end position of number
                end = (i,j-1)

                data['numbers'].append((int(number), (start, end)))

                # clear variables for next number
                number = ''
                start = None
                end = None

    for possible_gear in data['*']:
        adjacent_numbers = []
        for number in data['numbers']:
            if is_adjacent(possible_gear, number[1]):
                adjacent_numbers.append(number[0])

        if len(adjacent_numbers) == 2:
            total += adjacent_numbers[0] * adjacent_numbers[1]

    return total

def is_adjacent(possible_gear, number):
    # check if the possible gear is adjacent to the number
    for i in range(number[0][0] - 1, number[1][0] + 2):
        for j in range(number[0][1] - 1, number[1][1] + 2):
            if (i,j) == possible_gear:
                return True

    return False

if __name__ == '__main__':
    print(solve())