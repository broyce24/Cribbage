'''
Ben Royce
This is a program to emulate the game of Cribbage.
'''
from Card import Card
from random import shuffle, randint
import time
from itertools import chain, combinations

class Cribbage:
    def __init__(self):
        self.deck = [Card(r, s) for s in "SCHD" for r in range(1, 14)]
        shuffle(self.deck)
        self.player = []
        self.player_score = 0
        self.computer = []
        self.computer_score = 0
        self.crib = []
        self.table = []
        self.player_is_dealer = True
        self.flip_card = None

    def deal(self, player_deals = True):
        '''
        Deals cards based on the dealer.
        '''
        # Dealing cards. Non-dealer gets first card.
        print('You are the dealer.' if player_deals else 'Computer is the dealer.')
        for i in range(12):
            j = i if player_deals else i + 1  # neat trick to flip parity
            if j % 2:
                self.computer.append(self.deck.pop(0))
            else:
                self.player.append(self.deck.pop(0))
        self.player.sort(key=lambda c: c.rank)
        self.computer.sort(key=lambda c: c.rank)

        # Contributing cards to crib
        target = 'your' if player_deals else 'Computer\'s'
        print(f"Choose two cards to contribute to {target} crib.")
        for i in range(2):
            print("Hand:", self.player)
            crib_card = int(input(f"Type card index (1 to {6 - i}) to contribute it: "))
            self.crib.append(self.player.pop(crib_card - 1))
            self.crib.append(self.computer.pop(randint(0, 6 - i - 1)))  # Computer randomly chooses crib cards
        print("Selection:", self.crib[::2])  # Shows only the player's contribution

        # Cutting the deck
        if player_deals:
            cut = randint(0, 39)
            print(f"Computer chooses {cut} cards to cut.")
        else:
            cut = int(input("How many cards would you like to cut? Enter a number from 0-39: "))
            while True:  # this is just to catch numbers outside the cut range
                if 0 <= cut <= 39:
                    break
                else:
                    cut = int(input("Try again. Enter a number from 0-39: "))
            print(f"Cutting {cut} cards.")
        self.flip_card = self.deck[cut]

        # Printing information
        print("\nFlip card:", self.flip_card)
        print("Hand:", self.player)
        print("Computer hand:", self.computer)  # DEBUGGING
        print(f"{target} Crib:", self.crib)  # DEBUGGING

    def peg(self):
        #self.player = [Card(10, 'S'), Card(10, 'S'), Card(10, 'S'), Card(10, 'S')]
        #self.computer = [Card(10, 'S'), Card(10, 'S'), Card(10, 'S'), Card(10, 'S')] DeBUGGING
        # While players have cards left, alternate placing one card at a time until total of 31.
        # Make copies of the hands so the originals are unaffected
        player_hand = self.player.copy()
        computer_hand = self.computer.copy()
        total = 0

        def computer_plays(hand, tot):
            card_index = randint(0, len(hand) - 1)
            card = hand[card_index]
            if card.value + tot <= 31:
                chosen_card = card
            else:
                chosen_card = hand[0]
            print("Computer plays", chosen_card)
            self.table.append(hand.pop(card_index))
            tot += chosen_card.value
            print(self.table, "Sum =", tot)
            return hand, tot

        def player_plays(hand, tot):
            print("Available cards:", player_hand)
            while True:
                player_choice = int(input(f"Type card index (1 to {len(hand)}) to play: ")) - 1
                chosen_card = hand[player_choice]
                if chosen_card.value + tot <= 31:
                    break
                else:
                    print("Total must not exceed 31. Try again.")
            self.table.append(hand.pop(player_choice))
            tot += chosen_card.value
            print("You play", chosen_card)
            print(self.table, "Sum =", tot)
            return hand, tot

        # Non dealer goes first
        print("\nLet the pegging begin!")
        if self.player_is_dealer:
            computer_hand, total = computer_plays(computer_hand, total)
        players_turn = True

        # PEGGING FINALLY GOT IT TO ALTERNATE IN A LOOP
        while len(player_hand) or len(computer_hand):  # while someone has cards left
            time.sleep(1)
            player_can_play = len(player_hand) and (player_hand[0].value + total <= 31)
            computer_can_play = len(computer_hand) and (computer_hand[0].value + total <= 31)
            if players_turn and player_can_play:
                player_hand, total = player_plays(player_hand, total)
                players_turn = False if computer_can_play else True  # Needs to stay player's turn if computer can't play
            elif computer_can_play:
                computer_hand, total = computer_plays(computer_hand, total)
                players_turn = True
            else:
                print("End of stack!\n")
                self.table.clear()
                total = 0
        print("Pegging completed!")

    def score(self, hand=None):
        score = 0
        # Finding fifteens and pairs
        card_groups = list(chain.from_iterable(combinations(hand, r) for r in range(2, len(hand) + 1)))
        for group in card_groups:
            if sum(map(int, group)) == 15:
                score += 2
            if len(group) == 2 and group[0].rank == group[1].rank:
                score += 2

        # Find all runs by finding the difference between the values in each card group.
        # A run of three will be (1, 1), a run of four will be (1, 1, 1), etc.
        # We only need to do the groups of 3 or more cards, which will be indexes 10-25
        runs = {(-1, -1): 3, (-1, -1, -1): 4, (-1, -1, -1, -1): 5}
        for i in range(10, 26):
            group = card_groups[i]
            d = []
            for j in range(len(group) - 1):
                d.append(int(group[j]) - int(group[j+1]))
            tupled = tuple(d)
            if tupled in runs:
                score += runs[tupled]

        # Find flushes. We only need to check groups of 4 cards or more, which are indexes 20-25.
        for i in range(20, 26):
            if len({c.suit for c in card_groups[i]}) == 1:  # we have a flush
                if i == 25:  # this implies it's the group of 5 cards
                    score += 5
                else:
                    score += 4
        return score

    def scoring(self):
        if self.player_is_dealer:
            print("Computer's hand:", self.computer)
            print("Computer scores", score(self.computer))
            print("Your hand:", self.player)
            print("You score",  score(self.player))
            print("Your crib:", self.crib)
            print("Crib score:", score(self.crib))

def main():
    game = Cribbage()
    game.deal(False)
    game.peg()
    game.score()


if __name__ == '__main__':
    main()
