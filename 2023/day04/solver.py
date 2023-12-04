import sys

class Solver:
    def __init__(self, file_path = "test.txt"):
        # read input file
        with open(file_path) as f:
            self.lines = f.readlines()

        self.cards = []
        for line in self.lines:
            # create new card
            self.cards.append({'win' : set(), 'have': set()})
            
            # parse winning and "have" numbers
            [winning_numbers, have_numbers] = line.split(':')[1].split('|')
            
            # update winning cards set
            self.cards[-1]['win'].update(map(lambda x: int(x), winning_numbers.strip().split()))
            # update "have" cards set
            self.cards[-1]['have'].update(map(lambda x: int(x), have_numbers.strip().split()))

    def part1(self):
        total = 0

        for card in self.cards:
            # get number of matches by intersecting winning and "have" numbers
            number_of_matches = len(card['win'].intersection(card['have']))

            # add 2^(number_of_matches - 1) to total
            if number_of_matches >= 1:
                total += 1 << (number_of_matches - 1)

        return total
    
    def part2(self):
        # create dictionary of number of card copies
        card_copies = {x:1 for x in range(len(self.cards))}
        
        for i, card in enumerate(self.cards):
            # get number of matches by intersecting winning and "have" numbers
            number_of_matches = len(card['win'].intersection(card['have']))

            for j in range(1, number_of_matches + 1):
                # check if card index still exists
                if (i + j) < len(self.cards):
                    # add copies of the next number_of_matches cards
                    card_copies[i + j] += card_copies[i]

        return sum(card_copies.values())


if __name__ == '__main__':
    if len(sys.argv) > 1 and 1 <= int(sys.argv[1]) <= 2:
        if sys.argv[1] == '1':
            solver = Solver("input1.txt")
            print(solver.part1())
        else:
            solver = Solver("input1.txt")
            print(solver.part2())