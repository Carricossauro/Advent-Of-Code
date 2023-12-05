import sys

class Solver:
    def __init__(self, file_path = "test.txt"):
        # read input file
        with open(file_path) as f:
            self.lines = f.readlines()

        # get all the seeds to plant for part 1
        self.seeds = list(map(lambda x: int(x), self.lines[0].split(':')[1].strip().split(' ')))

        # get all the maps in order
        self.maps = []
        for line in self.lines[1:]:
            line = line.strip()
            if line != '':
                if 'map:' in line:
                    self.maps.append([])
                else:
                    self.maps[-1].append(tuple(map(lambda x: int(x), line.strip().split(' '))))

    # apply a map to a source
    def apply_map(self, source, map):
        for destination_start, source_start, range_length in map:
            # check if source is in range
            if source_start <= source < source_start + range_length:
                source = destination_start + (source - source_start)
                # mapping value has already been found, no need to continue
                break

        return source

    def part1(self):
        lowest_location = None

        # brute force each seed
        for seed in self.seeds:
            source = seed
            # apply all the maps consecutively
            for map in self.maps:
                source = self.apply_map(source, map)

            # check if this is the lowest location
            if lowest_location is None or lowest_location > source:
                lowest_location = source

        return lowest_location

    # this function fried my brain :(
    def find_next_ranges(self, ranges, map):
        next_ranges = []

        # "range-splitting"
        for start, length in ranges:
            mapped = False
            # check if this range is mapped by the map
            for destination_start, source_start, range_length in map:
                end = start + length - 1
                diff = start - source_start
                if source_start <= start < source_start + range_length:
                    mapped = True
                    if end <= source_start + range_length:
                        # the entire range is mapped here
                        next_ranges.append((destination_start + diff, length))
                        break
                    else:
                        # only part of the range is mapped here (starts in the map, ends after)
                        extra_length = end - (source_start + range_length)
                        next_ranges.append((destination_start + diff, length - extra_length))
                        ranges.append((source_start + range_length, extra_length))
                        break
                elif source_start <= end <= source_start + range_length:
                    # only part of the range is mapped here (starts before, ends in the map)
                    mapped = True
                    extra_length = source_start - start
                    next_ranges.append((destination_start, length - extra_length))
                    ranges.append((start, extra_length))
                    break
            
            # if no map was found, the range will remain the same
            if not mapped:
                next_ranges.append((start, length))

        return next_ranges

    def part2(self):
        ranges = list(zip(self.seeds[0::2], self.seeds[1::2]))

        for map in self.maps:
            ranges = self.find_next_ranges(ranges, map)

        return min([x[0] for x in ranges])

    
if __name__ == '__main__':
    if len(sys.argv) > 1 and 1 <= int(sys.argv[1]) <= 2:
        if sys.argv[1] == '1':
            solver = Solver("input1.txt")
            print(solver.part1())
        else:
            solver = Solver("input1.txt")
            print(solver.part2())