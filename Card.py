RANKS = {1: "A", 11: "J", 12: "Q", 13: "K"}
SUITS = {"S": "♠", "C": "♣", "H": "♥", "D": "♦"}


class Card:
    def __init__(self, rank: int, suit: str):
        self.rank = rank
        self.suit = suit
        self.value = min(10, rank)

    def __int__(self):
        return self.value

    def __repr__(self):
        if self.rank in RANKS:
            rank = RANKS[self.rank]
        else:
            rank = str(self.rank)
        return rank + SUITS[self.suit]
