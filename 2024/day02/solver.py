import sys

class Solver:
    def __init__(self, file_path = "test.txt"):
        # read input file
        with open(file_path) as f:
            self.lines = f.readlines()

        # parsing goes here
        self.reports = []
        for line in self.lines:
            line = line.strip()
            self.reports.append(list(map(int, line.split())))

    def part1(self):
        safe_reports = 0

        condition = {True: lambda x: x < 1 or x > 3, False: lambda x: x < -3 or x > -1}

        for report in self.reports:
            N_report = len(report)
            increasing = None

            for i in range(N_report):
                if i == 0:
                    continue
                
                diff = report[i] - report[i - 1]
                if i == 1:
                    increasing = diff > 0

                if condition[increasing](diff):
                    break
                
                if i == N_report - 1:
                    safe_reports += 1

        return safe_reports

    def part2(self):
        # i hate brute force solutions
        safe_reports = 0

        condition = {True: lambda x: x < 1 or x > 3, False: lambda x: x < -3 or x > -1}

        for report in self.reports:
            real_N_report = len(report)
            safe = False

            i_remove = -1
            while not safe and i_remove <= real_N_report - 1:
                # remove one element each step
                # start without removing an element
                new_report = report if i_remove == -1 else report[:i_remove] + report[i_remove + 1:]
                i_remove += 1

                # check if the new report is safe (without the removed element)
                N_report = len(new_report)
                increasing = None
                for i in range(N_report):
                    if i == 0:
                        continue
                    
                    diff = new_report[i] - new_report[i - 1]
                    if i == 1:
                        increasing = diff > 0

                    if condition[increasing](diff):
                        break
                    
                    if i == N_report - 1:
                        safe = True

            if safe == True:
                safe_reports += 1

        return safe_reports
    
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