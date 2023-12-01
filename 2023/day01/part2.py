import re

def solve():
    digits = {
        "one": 1, "two": 2, "three": 3,
        "four": 4, "five": 5, "six": 6,
        "seven": 7, "eight": 8, "nine": 9}
    
    expression = "(?=(one|two|three|four|five|six|seven|eight|nine|\d))"
    with open('day01/input2.txt') as f:
        lines = f.readlines()

        total = 0
        for line in lines:
            found_digits = [int(character) if character.isdigit() else digits[character] for character in re.findall(expression, line)]

            total += (found_digits[0] * 10) +  found_digits[-1]

    return total

if __name__ == '__main__':
    print(solve())