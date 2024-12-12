import sys

class Solver:
    def __init__(self, file_path = "test.txt"):
        # read input file
        with open(file_path) as f:
            self.lines = f.readlines()

        # parsing goes here
        self.plants = []

        for line in self.lines:
            self.plants.append(line.strip())

        self.N = len(self.plants)
        self.M = len(self.plants[0])

    def part1(self):
        # map search
        # at every step, look in each direction
        # if its still part of the region, check the new cell
        # if not, add to perimeter
        total = 0
        starts = [(i,j) for i in range(self.N) for j in range(self.M)]
        visited = set()

        for i_start, j_start in starts:
            if (i_start, j_start) in visited:
                continue

            area = 0
            perimeter = 0
            plant = self.plants[i_start][j_start]
            queue = [(i_start, j_start)]

            while queue:
                i, j = queue.pop()
                if (i, j) in visited:
                    continue
                visited.add((i, j))

                area += 1

                # top
                if i > 0 and self.plants[i - 1][j] == plant:
                    if (i - 1, j) not in visited:
                        queue.append((i - 1, j))
                else:
                    perimeter += 1

                # bottom
                if i < self.N - 1 and self.plants[i + 1][j] == plant:
                    if (i + 1, j) not in visited:
                        queue.append((i + 1, j))
                else:
                    perimeter += 1

                # left
                if j > 0 and self.plants[i][j - 1] == plant:
                    if (i, j - 1) not in visited:
                        queue.append((i, j - 1))
                else:
                    perimeter += 1

                # rigth
                if j < self.M - 1 and self.plants[i][j + 1] == plant:
                    if (i, j + 1) not in visited:
                        queue.append((i, j + 1))
                else:
                    perimeter += 1

            total += area * perimeter

        return total


    def part2(self):
        # this was surprisingly complicated
        # i feel like i cheated my way to the solution
        # calculate the area of the region with the same map search
        # at then end, sort the region by perimeter and move along counting sides
        # first do it vertical (top and bottom sides)
        # then horizontal (left and right sides)
        # there was probably a better way to do this
        total = 0
        starts = [(i,j) for i in range(self.N) for j in range(self.M)]
        visited = set()

        for i_start, j_start in starts:
            if (i_start, j_start) in visited:
                continue

            area = 0
            perimeter = 0
            plant = self.plants[i_start][j_start]
            queue = [(i_start, j_start)]

            for i, j in queue:
                if (i, j) in visited:
                    continue
                visited.add((i, j))

                area += 1

                # top
                if i > 0 and self.plants[i - 1][j] == plant:
                    if (i - 1, j) not in visited:
                        queue.append((i - 1, j))

                # bottom
                if i < self.N - 1 and self.plants[i + 1][j] == plant:
                    if (i + 1, j) not in visited:
                        queue.append((i + 1, j))

                # left
                if j > 0 and self.plants[i][j - 1] == plant:
                    if (i, j - 1) not in visited:
                        queue.append((i, j - 1))

                # rigth
                if j < self.M - 1 and self.plants[i][j + 1] == plant:
                    if (i, j + 1) not in visited:
                        queue.append((i, j + 1))

            region = set(queue)

            # sort the region by position
            queue.sort()
            top = False
            bottom = False
            
            # move along the positions counting the sides
            # when a cell does not belong, reset side flags
            # since the next side will be a different one
            for i in range(self.N):
                for j in range(self.M):
                    if (i, j) in queue:
                        if (i - 1, j) in region:
                            top = False
                        elif not top:
                            top = True
                            perimeter += 1
                        
                        if (i + 1, j) in region:
                            bottom = False
                        elif not bottom:
                            bottom = True
                            perimeter += 1
                    else:
                        top = False
                        bottom = False

            # sort the region by position
            # vertical first since we will be moving by column
            queue.sort(key=lambda x: (x[1], x[0]))
            right = False
            left = False

            # move along the positions counting the sides
            # when a cell does not belong, reset side flags
            # since the next side will be a different one
            for j in range(self.M):
                for i in range(self.N):
                    if (i, j) in queue:
                        if (i, j + 1) in region:
                            right = False
                        elif not right:
                            right = True
                            perimeter += 1
                        
                        if (i, j - 1) in region:
                            left = False
                        elif not left:
                            left = True
                            perimeter += 1
                    else:
                        right = False
                        left = False
            
            total += area * perimeter

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