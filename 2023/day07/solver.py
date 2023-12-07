import sys

FIVE = 6
FOUR = 5
FULL_HOUSE = 4
THREE = 3
TWO_PAIRS = 2
PAIR = 1
HIGH_CARD = 0

values = {
    '2': 2, '3': 3, '4': 4,
    '5': 5, '6': 6, '7': 7,
    '8': 8, '9': 9, "T": 10,
    "J": 11, "Q": 12, "K": 13,
    "A": 14
}

class Hand:
    def __init__(self, cards, bid):
        self.cards = cards
        self.bid = bid

        self.count = {}
        for card in self.cards:
            if card not in self.count:
                self.count[card] = 0
            self.count[card] += 1

    # function to compare two hands
    def __lt__(self, other):
        if self.type() < other.type():
            return True
        elif self.type() > other.type():
            return False

        # same type
        # compare hands based on the values of each card
        return tuple(map(lambda x: values[x], self.cards)) < tuple(map(lambda x: values[x], other.cards))
    
    # function to compare two hands
    def __eq__(self, other):
        return self.cards == other.cards

    # function to determine the type of the hand
    def type(self):
        count = self.count

        counts = count.values()
        if 5 in counts:
            return FIVE
        elif 4 in counts:
            return FOUR
        elif 3 in counts and 2 in counts:
            return FULL_HOUSE
        elif 3 in counts:
            return THREE
        elif list(counts).count(2) == 2:
            return TWO_PAIRS
        elif 2 in counts:
            return PAIR
        else:
            return HIGH_CARD


class Hand2(Hand):
    # function to determine the type of the hand in part 2
    def type(self):
        count = self.count

        counts = count.values()
        if 'J' not in count.keys():
            # J is not in the hand, use the original type function
            return Hand.type(self)
        elif count['J'] == 5 or count['J'] == 4:
            # there are 4 or 5 J's, so the type is always Five of a Kind
            return FIVE
        elif count['J'] == 3:
            # there are 3 J's, so there can be a Five of a Kind or a Four of a Kind
            if 2 in counts:
                return FIVE
            else:
                return FOUR
        elif count['J'] == 2:
            # there are 2 J's, so there can be a Five of a Kind, a Four of a Kind or a Three of a Kind
            if 3 in counts:
                return FIVE
            elif list(counts).count(2) == 2:
                return FOUR
            else:
                return THREE
        else:
            # There is only 1 J, so there can be a Five of a Kind, a Four of a Kind, a Full House, a Three of a Kind or a Pair
            if 4 in counts:
                return FIVE
            elif 3 in counts:
                return FOUR
            elif list(counts).count(2) == 2:
                return FULL_HOUSE
            elif 2 in counts:
                return THREE
            else:
                return PAIR


class Solver:
    def __init__(self, file_path = "test.txt"):
        # read input file
        with open(file_path) as f:
            self.lines = f.readlines()

        self.hands = []
        self.hands2 = []
        for line in self.lines:
            [cards, bid] = line.split(' ')

            # store the hand for both parts
            self.hands.append(Hand(cards, int(bid)))
            self.hands2.append(Hand2(cards, int(bid)))

    def part1(self):
        total = 0
        # rank the hands
        self.hands.sort()

        for i, hand in enumerate(self.hands):
            total += hand.bid * (i + 1)

        return total

    def part2(self):
        # change J to the lowest value card
        values['J'] = 1

        self.hands = self.hands2

        return self.part1()

if __name__ == '__main__':
    if len(sys.argv) > 1 and 1 <= int(sys.argv[1]) <= 2:
        if sys.argv[1] == '1':
            solver = Solver("input1.txt")
            print(solver.part1())
        else:
            solver = Solver("input1.txt")
            print(solver.part2())