from Card import Card

c1 = Card(5, "D")
c2 = Card(10, "C")
c3 = Card(8, "H")
c4 = Card(9, "D")
c5 = Card(9, "C")
c6 = Card(9, "C")
c7 = Card(9, "S")
test_hand = [c1, c2, c3, c4, c5, c6, c7]
table = []


def play() -> None:
    def is_run(cards: list[Card], sorted: bool) -> bool:
        if not sorted:
            cards.sort(key = lambda c: c.rank)
        
        # figure out if a list of unordered cards is a run.
        pass
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
        if sum(map(lambda c: c.rank, table)) == 15:
            print("Fifteen!")
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
        #if cards_down > 2 and is_run(table[])
    print(table, "score:", score)

play()
