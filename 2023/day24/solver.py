import sys
import z3

class Solver:
    def __init__(self, file_path = "test.txt"):
        # read input file
        with open(file_path) as f:
            self.lines = f.readlines()

        self.hail = []
        self.velocity = []
        for line in self.lines:
            [hail, velocity] = line.split("@")
            hail = tuple(map(int, hail.strip().split(', ')))
            velocity = tuple(map(int, velocity.strip().split(', ')))

            self.hail.append(hail)
            self.velocity.append(velocity)

        self.min_range = 7 if file_path == "test.txt" else 200000000000000
        self.max_range = 27 if file_path == "test.txt" else 400000000000000

    # for each pair of hails, find the time of collision, if any
    # if the collision is in the future, check if it is in the range
    # if the collision is in the past, ignore it
    def find_collisions(self, min_range, max_range):
        self.collisions = 0

        for i in range(len(self.hail)):
            (a1, b1, c1) = self.hail[i]
            (vx1, vy1, vz1) = self.velocity[i]

            for j in range(i + 1, len(self.hail)):
                (a2, b2, c2) = self.hail[j]
                (vx2, vy2, vz2) = self.velocity[j]
                
                # { a1 + vx1 * k = a2 + vx2 * k2
                # { b1 + vy1 * k = b2 + vy2 * k2
                # https://imgur.com/a/rj80A9N
                A = b2 + vy2 * ((a1 - a2) / vx2) - b1
                B = vy1 - vy2 * (vx1 / vx2)
                if B != 0:
                    k1 = A / B
                    k2 = (a1 + vx1 * k1 - a2) / vx2

                    # guarantee that the path intersection is in the future
                    if k1 > 0 and k2 > 0:
                        x1 = a1 + vx1 * k1
                        y1 = b1 + vy1 * k1

                        if min_range <= x1 <= max_range and min_range <= y1 <= max_range:
                            self.collisions += 1

    def part1(self):
        self.find_collisions(self.min_range, self.max_range)

        return self.collisions

    # find the ideal position and velocity of the thrown rock
    # use z3 to solve the system of equations for intersection of paths
    def find_ideal_position(self):
        number_of_hails = 3

        # create z3 variables
        a, b, c = z3.Ints('a b c')
        vx, vy, vz = z3.Ints('vx vy vz')
        ks = []
        for k in range(number_of_hails):
            ks.append(z3.Int('k' + str(k + 1)))

        solver = z3.Solver()

        for i in range(number_of_hails):
            solver.add(self.hail[i][0] + self.velocity[i][0] * ks[i] == a + vx * ks[i])
            solver.add(self.hail[i][1] + self.velocity[i][1] * ks[i] == b + vy * ks[i])
            solver.add(self.hail[i][2] + self.velocity[i][2] * ks[i] == c + vz * ks[i])

        total = 0
        if solver.check() == z3.sat:
            model = solver.model()
            print(model[a], model[b], model[c])
            print(model[vx], model[vy], model[vz])
            total = model[a].as_long() + model[b].as_long() + model[c].as_long()

        return total

    def part2(self):
        return self.find_ideal_position()
    
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