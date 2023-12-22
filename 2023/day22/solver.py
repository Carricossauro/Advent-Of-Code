import sys

class Solver:
    def __init__(self, file_path = "test.txt"):
        # read input file
        with open(file_path) as f:
            self.lines = f.readlines()

        self.bricks = []
        name = 0
        for line in self.lines:
            [start, end] = list(map(lambda x: x.split(','), line.strip().split('~')))

            self.bricks.append((name, tuple(map(int, start)), tuple(map(int, end))))

            # this was unnecessary, could have just used the index of the brick in the list
            name = name + 1

        # sort bricks by z coordinate
        # this is necessary because we need to drop bricks starting from the lowest
        self.bricks.sort(key=lambda x: (x[1][2], x[2][2]))

    # check if two bricks share x coordinates
    def share_x(self, brick1, brick2):
        sx1, sy1, sz1 = brick1[1]
        ex1, ey1, ez1 = brick1[2]

        sx2, sy2, sz2 = brick2[1]
        ex2, ey2, ez2 = brick2[2]

        return sx1 <= sx2 <= ex1 or sx1 <= ex2 <= ex1 or sx2 <= sx1 <= ex2 or sx2 <= ex1 <= ex2
    
    # check if two bricks share y coordinates
    def share_y(self, brick1, brick2):
        sx1, sy1, sz1 = brick1[1]
        ex1, ey1, ez1 = brick1[2]

        sx2, sy2, sz2 = brick2[1]
        ex2, ey2, ez2 = brick2[2]

        return sy1 <= sy2 <= ey1 or sy1 <= ey2 <= ey1 or sy2 <= sy1 <= ey2 or sy2 <= ey1 <= ey2

    # check if new position for brick1 is compatible with brick2
    def overlap(self, brick1, brick2):
        sx1, sy1, sz1 = brick1[1]
        ex1, ey1, ez1 = brick1[2]

        sx2, sy2, sz2 = brick2[1]
        ex2, ey2, ez2 = brick2[2]
    	
        # check if brick1 shares some z with brick2
        # opposite doesn't need to be checked because the bricks are sorted by z coordinate
        if sz1 <= ez2:
            # bricks only overlap if they share coordinates in both axis
            if self.share_x(brick1, brick2) and self.share_y(brick1, brick2):
                return True
            
        return False

    # drop all bricks to their lowest point
    def freefall(self):
        self.support = {brick[0]: set() for brick in self.bricks}

        for i, brick in enumerate(self.bricks):
            name = brick[0]
            sx, sy, sz = brick[1]
            ex, ey, ez = brick[2]

            below_sz = sz - 1
            below_ez = ez - 1
            valid = below_sz >= 1

            # drop brick one by one until it overlaps with another brick (supporter)
            while valid:
                supporters = set()
                for j in range(i):
                    # if brick is supported by another brick, add it to the supporters set at this height (sz)
                    if self.overlap((name, (sx, sy, below_sz), (ex, ey, below_ez)), self.bricks[j]):
                        valid = False
                        supporters.add(self.bricks[j][0])

                if valid:
                    # if brick is not supported by any other brick, drop it one level and check again
                    sz = below_sz
                    ez = below_ez
                    below_sz -= 1
                    below_ez -= 1
                    valid = below_sz >= 1
                else:
                    # when we reach the lowest height for this brick,
                    # add all supporters to the support dictionary
                    self.support[name] = supporters

            self.bricks[i] = (name, (sx, sy, sz), (ex, ey, ez))

    def part1(self):
        self.freefall()
        total = 0
        
        # count bricks that can be desintegrated without dropping any other brick
        for brick in self.bricks:
            name = brick[0]
            can_be_desintegrated = True

            for supporters in self.support.values():
                # if a brick is supported by only one other brick, the one that supports it can't be desintegrated
                if name in supporters and len(supporters) < 2:
                    can_be_desintegrated = False
                    break

            if can_be_desintegrated:
                total += 1

        return total

    def part2(self):
        self.freefall()
        fall = {brick[0]: 0 for brick in self.bricks}

        # sequentially drop bricks starting from each one
        for brick in self.bricks:
            name = brick[0]
            
            fallen_bricks = set([name])
            for new_brick in self.bricks:
                # only drop brick if it's not the same as the one we're dropping
                # and if it's supported by any of the previously fallen bricks
                if brick != new_brick and self.support[new_brick[0]] and all([b in fallen_bricks for b in self.support[new_brick[0]]]):
                    fallen_bricks.add(new_brick[0])
                    fall[name] += 1

        # for each brick, add the number of bricks it supports (directly or indirectly)
        return sum(fall.values())
    
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