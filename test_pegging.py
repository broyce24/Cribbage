from Card import Card

c1 = Card(5, "D")
c2 = Card(10, "C")
c3 = Card(8, "H")
c4 = Card(9, "D")
c5 = Card(9, "C")
test_hand = [c1, c2, c3, c4, c5]
table = []
score = 0


def play():
    while len(test_hand) > 0:
        print(table, "score:", score)
        c_index = int(input(f"Select from {test_hand} "))
        if c_index == -1:
            return
        table.append(test_hand.pop(c_index))
        if len(table) == 1:
            continue
        if sum(map(lambda c: c.rank, table)) == 15:
            score += 2
