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
test_hand = [c1, c2, c3, c4, c5, c6, c7]
table = []


def is_run(cards):
    cards.sort(key=lambda c: c.rank)
    for i in range(len(cards) - 1):
        if cards[i].rank - cards[i + 1].rank != -1:
            return False
    return True


def play() -> None:
    # test cases: 5, 5, 1, 2, 3


    score = 0
    ongoing_run = False
    while len(test_hand) > 0:
        print(table, "score:", score)
        c_index = int(input(f"Select from {test_hand} "))
        if c_index == -1:  # Quit command
            return
        table.append(test_hand.pop(c_index))
        cards_down = len(table)
        if cards_down == 1:
            continue
        # Scoring below
        if sum(map(int, table)) == 15:
            print("Fifteen!")
            score += 2
        elif sum(map(int, table)) == 31:
            print("Thirty one!")
            score += 2
        if table[-1].rank == table[-2].rank:
            if cards_down > 2 and table[-2].rank == table[-3].rank:
                if cards_down > 3 and table[-3].rank == table[-4].rank:
                    print("Quads!")
                    score += 12
                else:
                    print("Trips!")
                    score += 6
            else:
                print("Pair!")
                score += 2
        if cards_down > 2:
            run_length = 3
            while run_length <= cards_down and is_run(table[-run_length:]):
                run_length += 1
            print(f"Run of {run_length - 1}!")
            score += run_length
    print(table, "score:", score)


def main():
    play()

if __name__ == '__main__':
    main()
# Need to add hitting 31 as a score in pegging
# Need to recognize runs that don't start at the first card
# Also do I need the self.player_is_dealer thing?
