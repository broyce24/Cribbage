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
        self.computer = []
        self.crib = []
        self.table = []
        self.player_deals = True
        self.flip_card = None

    # Player is player on first turn
    def deal(self):
        '''
        Implements the function for dealing cards and selecting crib cards each round.
        '''
        print("\nDealing cards...")
        for i in range(12):
            if i % 2:
                # Non-player gets first card
                self.computer.append(self.deck.pop(0))
            else:
                self.player.append(self.deck.pop(0))
        self.player.sort(key=lambda c: c.rank)
        self.computer.sort(key=lambda c: c.rank)

        if self.player_deals:
            print("Choose two cards to contribute to your crib.")
        else:
            print("Choose two cards to contribute to the dealer's crib.")
        for i in range(2):
            print("Hand:", self.player)
            crib_card = int(input(f"Type card index (1 to {6 - i}) to contribute it: "))
            self.crib.append(self.player.pop(crib_card - 1))
            self.crib.append(self.computer.pop(randint(0, 6 - i - 1)))
        print("Selection:", self.crib[::2])

        if self.player_deals:
            cut = randint(0, 39)
            print(f"Opponent chooses {cut} cards to cut.")
        else:
            cut = int(input("Please choose the number of cards to cut (0-39): "))
        self.flip_card = self.deck[cut]
        print("\nFlip card:", self.flip_card)
        print("Hand:", self.player)
        print("Computer hand:", self.computer)

    def peg(self):
        # While players have cards left, alternate placing one card at a time until total of 31.
        # Make copies of the hands so the originals are unaffected
        player_hand = self.player.copy()
        computer_hand = self.computer.copy()
        players_turn = not self.player_deals
        player_can_play = True
        computer_can_play = True
        total = 0

        def computer_plays():
            nonlocal total
            card_index = randint(0, len(computer_hand) - 1)
            card = computer_hand[card_index]
            if card.value + total <= 31:
                chosen_card = card
            else:
                chosen_card = computer_hand[0]

            print("Computer plays", chosen_card)
            self.table.append(computer_hand.pop(card_index))
            total += chosen_card.value
            print()
            print(self.table, "Sum =", total)

        def player_plays():
            nonlocal total
            print("Available cards:", player_hand)
            while True:
                player_choice = int(input(f"Type card index (1 to {len(player_hand)}) to play: ")) - 1
                chosen_card = player_hand[player_choice]
                if chosen_card.value + total > 31:
                    print("Total must not exceed 31. Try again.")
                else:
                    break
            self.table.append(player_hand.pop(player_choice))
            total += chosen_card.value
            print("You play", chosen_card)
            print()
            print(self.table, "Sum =", total)
            print()

        # Non dealer goes first
        print("\nLet the pegging begin!")

        while len(player_hand) or len(computer_hand):
            player_can_play = len(player_hand) and (player_hand[0].value + total <= 31)
            if players_turn:
                if player_can_play:
                    player_plays()
                else:
                    print("You cannot play.")
                players_turn = not players_turn
                computer_can_play = len(computer_hand) and (computer_hand[0].value + total <= 31)
            if computer_can_play:
                # Computer picks a random card if it can play. If that card would go over 31, it uses the lowest card.
                computer_plays()
                players_turn = not players_turn
            else:
                print("Your opponent cannot play.")
                players_turn = not players_turn
            print()
            if total == 31 or (not player_can_play and not computer_can_play):
                print("End of stack!")
                print(self.table, "Sum =", total, end="\n\n\n")
                self.table.clear()
                total = 0
        print("Pegging completed!")

    def test_scoring(self):
        score = 0
        # 15 for 2, 15 for 4, 15 for 6, pair for 8
        hand = [Card(5, 'H'), Card(7, 'D'), Card(7, 'H'), Card(8, 'D'), Card(9, 'D')]
        # Use the powerset (n >= 2) of the list to find all card combos
        def powerset(s):
            return chain.from_iterable(combinations(s, r) for r in range(2, len(s) + 1))
        # Check the sum of each powerset. If it's 15, add +2 to the score.
        card_groups = list(powerset(hand))
        print(card_groups)
        for t in card_groups:
            total = 0
            for card in t:
                total += int(card)
            if total == 15:
                score += 2
        print(score)
        # Find all pairs
        for t in card_groups:
            if len(t) == 2:
                if t[0].get_rank() == t[1].get_rank():
                    score += 2
        # Find all runs by converting the combos to their values and seeing if they're in the list 1-14
        all_nums = tuple(range(0, 15))
        print(set((1, 2, 3)).issubset((0, 1, 2, 3, 4, 5)))


def main():
    game = Cribbage()
    game.test_scoring()


if __name__ == '__main__':
    main()
