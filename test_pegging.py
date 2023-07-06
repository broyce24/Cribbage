from Card import Card
import time
from itertools import chain, combinations

c1 = Card(1, "D")
c2 = Card(2, "C")
c3 = Card(3, "H")
c4 = Card(4, "D")
c5 = Card(5, "C")
c6 = Card(6, "C")
c7 = Card(7, "S")
c8 = Card(7, "S")
c9 = Card(7, "S")
c10 = Card(7, "S")
test_hand = [c1, c2, c3, c4, c5, c6, c7, c8, c9, c10]

self.table = []


def is_run(cards):
    cards.sort(key=lambda c: c.rank)
    for i in range(len(cards) - 1):
        if cards[i].rank - cards[i + 1].rank != -1:
            return False
    return True


def play():
    # test cases: 5, 5, 1, 2, 3

    score = 0
    ongoing_run = False
    while len(test_hand) > 0:
        print(self.table, "score:", score)
        c_index = int(input(f"Select from {test_hand} "))
        if c_index == -1:  # Quit command
            return
        self.table.append(test_hand.pop(c_index))
        cards_down = len(self.table)
        if cards_down == 1:
            continue
        # Scoring below
        if sum(map(int, self.table)) == 15:
            print("Fifteen!")
            score += 2
        elif sum(map(int, self.table)) == 31:
            print("Thirty one!")
            score += 2
        if self.table[-1].rank == self.table[-2].rank:
            if cards_down > 2 and self.table[-2].rank == self.table[-3].rank:
                if cards_down > 3 and self.table[-3].rank == self.table[-4].rank:
                    print("Quads!")
                    score += 12
                else:
                    print("Trips!") #
                    score += 6
            else:
                print("Pair!")
                score += 2
        if cards_down > 2:
            for i in range(cards_down - 2):
                if is_run(self.table[i:]):
                    run_length = cards_down - i
                    print(f"Run of {run_length}!")
                    score += run_length
                    break
    print(self.table, "score:", score)


def main():
    play()

if __name__ == '__main__':
    main()

# Need to add hitting 31 as a score in pegging
# Need to recognize runs that don't start at the first card
# Also do I need the self.player_is_dealer thing?
