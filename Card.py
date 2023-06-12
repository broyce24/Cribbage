class Card:
    """
    Represents a playing card.
    """

    def __init__(self, rank: int, suit: str):
        self.rank = rank
        self.suit = suit
        self.value = min(10, rank)

    def __int__(self):
        return self.value

    def __repr__(self):
        """
        Returns the string representation of a card using emojis

        Ex: 5 of Clubs
        """
        ranks = {1: "A", 11: "J", 12: "Q", 13: "K"}
        if self.rank in ranks:
            rank = ranks[self.rank]
        else:
            rank = str(self.rank)

        suits = {"S": "♠", "C": "♣", "H": "♥", "D": "♦"}
        return rank + suits[self.suit]
