import sys

class Solver:
    def __init__(self, file_path = "test.txt"):
        # read input file
        with open(file_path) as f:
            self.lines = f.readlines()

        # parsing goes here
        self.rules = {}             # this stores the rules as is from the input, i.e., what pages come before a page
        self.reversed_rules = {}    # this stores the rules in reversr order, i.e., what pages come after a page
        self.updates = []           # this stores the updates as is from the input

        rules = True
        for line in self.lines:
            if line == '\n':
                rules = False
                continue

            if rules:
                rule = list(map(int, line.strip().split('|')))
                if rule[0] not in self.rules:
                    self.rules[rule[0]] = set()
                self.rules[rule[0]].add(rule[1])

                if rule[1] not in self.reversed_rules:
                    self.reversed_rules[rule[1]] = set()
                self.reversed_rules[rule[1]].add(rule[0])
            else:
                self.updates.append(list(map(int, line.strip().split(','))))

    def part1(self):
        # pretty simple strategy
        # for each page, check if any of the previous ones shouldn't be there
        total = 0

        for update in self.updates:
            current_pages = set()

            valid_update = True
            N = 0
            # loop through each page in the update
            for page in update:
                N += 1
                # check if there is any restriction on the page
                if page in self.rules:
                    # loop through the pages that come after
                    for rule_page in self.rules[page]:
                        # check if those pages are already in the current pages
                        # if they are, it's invalid
                        if rule_page in current_pages:
                            valid_update = False
                            break
                
                # if the update is still valid, add the page to the current pages
                # if not, break the loop to avoid unnecessary checks
                if valid_update:
                    current_pages.add(page)
                else:
                    break

            # if the update is valid, add the middle page to the total
            if valid_update:
                total += update[N // 2]

        return total

    def part2(self):
        # i did not at first realize that the rules include cycles
        # so i had to change the order calculation to be specific to individual updates
        # anyway, this basically orders each page based on the rules it's involved in
        total = 0

        for update in self.updates:
            order = {} # this stores the order that pages may come in

            applicable = set(update) # this stores the pages that are in the update (but is more efficient than using a list)
            queue = list(update) # this stores the pages that are yet to be checked + the pages whose previous pages have been changed
            for left in queue:
                if left not in order:
                    # if the page is not in the order, it means it has not been checked yet
                    order[left] = 0
                elif left in self.reversed_rules:
                    # else, if the page is in the reversed rules, we need to find the correct order position
                    before_left = list(filter(lambda x: x in order and x in applicable, self.reversed_rules[left]))
                    if len(before_left) > 0:
                        order[left] = max([order[x] for x in before_left]) + 1

                if left in self.rules:
                    # if the page has restrictions on what cannot come before it, we need to (re)check those pages
                    for right in self.rules[left]:
                        if right in applicable:
                            if right not in order:
                                queue.append(right)
                            elif order[right] <= order[left]:
                                queue.append(right)

            # from here on, it's the same as part 1 but we sort the update basedon the order calculated
            # and only count the originally invalid updates
            current_pages = set()

            valid_update = True
            N = len(update)
            for page in update:
                if page in self.rules:
                    for rule_page in self.rules[page]:
                        if rule_page in current_pages:
                            valid_update = False
                            break
                
                if valid_update:
                    current_pages.add(page)
                else:
                    break

            if not valid_update:
                update.sort(key=lambda x: order[x])
                total += update[N // 2]

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