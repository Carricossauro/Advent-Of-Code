import sys
import re

class Solver:
    def __init__(self, file_path = "test.txt"):
        # read input file
        with open(file_path) as f:
            self.lines = f.readlines()

        number_expression = r"(\d+)"
        times = re.findall(number_expression, self.lines[0])
        distances = re.findall(number_expression, self.lines[1])

        self.races = list(zip(map(int, times), map(int, distances)))
        self.single_race = (int("".join(times)), int("".join(distances)))

    def part1(self):
        total = 1
        
        for race_time, race_record in self.races:
            total_race = 0
            
            # find everytime that the distance is greater than the record
            for button in range(race_record):
                time_left = race_time - button
                distance = button * (time_left)

                if distance > race_record:
                    # distance is greater than the record
                    total_race += 1
            
            total *= total_race

        return total

    # this is the same as part1, but with a different way to calculate the total
    def part2(self):
        total = 0
        race_time, race_record = self.single_race

        # find the first time that the distance is greater than the record
        for button in range(race_record):
            time_left = race_time - button
            distance = button * (time_left)

            if distance > race_record:
                # the first time that the distance is greater than the record
                break
        
        total = race_time - button*2 + 1

        return total
    
if __name__ == '__main__':
    if len(sys.argv) > 1 and 1 <= int(sys.argv[1]) <= 2:
        if sys.argv[1] == '1':
            solver = Solver("input1.txt")
            print(solver.part1())
        else:
            solver = Solver("input1.txt")
            print(solver.part2())