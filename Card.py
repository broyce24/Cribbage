class Card:
    '''
    Represents a playing card.
    '''
    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit
        self.value = 10 if rank > 10 else rank

    def __int__(self):
        return self.value

    def __repr__(self):
        '''
        Returns the string representation of a card using emojis

        Ex: 5 of Clubs
        '''
        match self.rank:
            case 1:
                rank = 'A'
            case 11:
                rank = 'J'
            case 12:
                rank = 'Q'
            case 13:
                rank = 'K'
            case _:
                rank = str(self.rank)

        match self.suit:
            case 'S':
                return rank + '♠'
            case 'C':
                return rank + '♣'
            case 'H':
                return rank + '♥'
            case 'D':
                return rank + '♦'

    def get_rank(self):
        return self.rank