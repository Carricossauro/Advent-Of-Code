import sys

class Solver:
    def __init__(self, file_path = "test.txt"):
        # read input file
        with open(file_path) as f:
            self.lines = f.readlines()

        self.workflows = {}
        self.parts = []
        reading_parts = False
        for line in self.lines:
            if line == '\n':
                reading_parts = True
                continue
            
            if reading_parts:
                # parse part
                part = {}
                part_numbers = line.strip()[1:-1].split(",")
                for part_number in part_numbers:
                    variable = part_number[0]
                    number = int(part_number[2:])
                    part[variable] = number
                
                # always start at 'in'
                part['workflow'] = 'in'
                self.parts.append(part)
            else:
                # parse workflow
                workflow = []
                [name, rest] = line.strip().split("{")
                rules = rest[:-1].split(",")
                for rule in rules[:-1]:
                    [rule_condition, rule_target] = rule.split(":")
                    variable = rule_condition[0]
                    condition = rule_condition[1]
                    number = int(rule_condition[2:])
                    
                    # add lambda function to workflow (facilitates checking rules)
                    if condition == '<':
                        function = lambda x, var, n: x[var] < n
                    elif condition == '>':
                        function = lambda x, var, n: x[var] > n

                    # add rule to workflow
                    workflow.append((function, variable, number, rule_target, condition))

                # add the last rule to the workflow, no condition (always True)
                workflow.append((lambda x, var, n: True, 'a', 0, rules[-1], None))

                self.workflows[name] = workflow

    def part1(self):
        total = 0
        
        for part in self.parts:
            # find each part's final workflow
            while part['workflow'] not in ['A', 'R']:
                for function, variable, number, target, _condition in self.workflows[part['workflow']]:
                    # if the function returns true, then this rule applies to this part
                    if function(part, variable, number):
                        # change the part's workflow to the target
                        part['workflow'] = target
                        break

            # add up the total for each part that ends in 'A'
            if part['workflow'] == 'A':
                total += part['x'] + part['m'] + part['a'] + part['s']

        return total

    # run same algorithm as part 1 but for ranges instead of specific parts
    def part2(self):
        total = 0
        parts = [{'x': (1, 4000), 'm': (1, 4000), 'a': (1, 4000), 's': (1, 4000), 'workflow': 'in'}]

        for part in parts:
            if part['workflow'] == 'A':
                total_part = 1
                # x
                total_part *= part['x'][1] - part['x'][0] + 1
                # m
                total_part *= part['m'][1] - part['m'][0] + 1
                # a
                total_part *= part['a'][1] - part['a'][0] + 1
                # s
                total_part *= part['s'][1] - part['s'][0] + 1

                total += total_part
                continue
            elif part['workflow'] == 'R':
                continue

            for _function, variable, number, target, condition in self.workflows[part['workflow']]:
                (minimum, maximum) = part[variable]
                if condition == '<':
                    # split the range into two parts
                    min_range = (minimum, number - 1)
                    max_range = (number, maximum)

                    # range under 'number' will get the new workflow
                    parts.append({**part, variable: min_range, 'workflow': target})

                    # range over 'number' will keep the same workflow and continue searching rules
                    part[variable] = max_range
                elif condition == '>':
                    # split the range into two parts
                    min_range = (minimum, number)
                    max_range = (number + 1, maximum)

                    # range over 'number' will get the new workflow
                    parts.append({**part, variable: max_range, 'workflow': target})

                    # range under 'number' will keep the same workflow and continue searching rules
                    part[variable] = min_range

            # add the part back to the list with the final target of the workflow
            parts.append({**part, 'workflow': target})

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