def solve():
    # read in the input
    with open('day03/input1.txt', 'r') as f:
        lines = f.readlines()

    # get the number of rows and columns
    N = len(lines)
    M = len(lines[0].strip())

    total = 0
    for i, line in enumerate(lines):
        number = ''
        start = None # start position of number
        end = None # end position of number

        for j, char in enumerate(line):
            if char.isdigit():
                # if the start position of the number has not been set, set it
                if not number:
                    start = (i,j)

                number += char
            elif number != '':
                # set end position of number
                end = (i,j-1)

                adjacent_positions = get_adjacent_positions(N, M, start, end, lines)
                for x, y in adjacent_positions:
                    if lines[x][y] != '.' and not lines[x][y].isdigit():
                        total += int(number)
                        break

                # clear variables for next number
                number = ''
                start = None
                end = None
    
    return total

# function made by github copilot lol
def get_adjacent_positions(N, M, start, end, lines):
    adjacent_positions = []
    for i in range(start[0] - 1, end[0] + 2):
        for j in range(start[1] - 1, end[1] + 2):
            # check if the position is within the bounds of the grid
            if i >= 0 and i < N and j >= 0 and j < M:
                # check if the position is not between the start and end positions
                if not (i >= start[0] and i <= end[0] and j >= start[1] and j <= end[1]):
                    adjacent_positions.append((i,j))

    return adjacent_positions

if __name__ == '__main__':
    print(solve())