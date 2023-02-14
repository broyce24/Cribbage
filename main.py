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
        self.player_is_dealer = True
        self.flip_card = None

    def player_deals(self):
        '''
        Deals cards when player is the dealer.
        '''
        print("\nYou are the dealer.")

        for i in range(12):
            if i % 2:
                # Computer gets the first card
                self.computer.append(self.deck.pop(0))
            else:
                self.player.append(self.deck.pop(0))
        self.player.sort(key=lambda c: c.rank)
        self.computer.sort(key=lambda c: c.rank)

        print("Choose two cards to contribute to your crib.")
        for i in range(2):
            print("Hand:", self.player)
            crib_card = int(input(f"Type card index (1 to {6 - i}) to contribute it: "))
            self.crib.append(self.player.pop(crib_card - 1))
            self.crib.append(self.computer.pop(randint(0, 6 - i - 1)))  # Computer randomly chooses crib cards
        print("Selection:", self.crib[::2])  # Shows only the player's contribution

        cut = randint(0, 39)
        print(f"Opponent chooses {cut} cards to cut.")
        self.flip_card = self.deck[cut]
        print("\nFlip card:", self.flip_card)
        print("Hand:", self.player)
        print("Computer hand:", self.computer)  # DEBUGGING

    def computer_deals(self):
        '''
        Deals cards when computer is the dealer.
        '''
        print('Opponent is the dealer.')
        self.player_is_dealer = False
        for i in range(12):
            if i % 2:
                # Player gets the first card
                self.player.append(self.deck.pop(0))
            else:
                self.computer.append(self.deck.pop(0))
        self.player.sort(key=lambda c: c.rank)
        self.computer.sort(key=lambda c: c.rank)

        print("Choose two cards to contribute to Opponent's crib.")
        for i in range(2):
            print("Hand:", self.player)
            crib_card = int(input(f"Type card index (1 to {6 - i}) to contribute it: "))
            self.crib.append(self.player.pop(crib_card - 1))
            self.crib.append(self.computer.pop(randint(0, 6 - i - 1)))  # Computer randomly chooses crib cards
        print("Selection:", self.crib[::2])  # Shows only the player's contribution

        cut = int(input("How many cards would you like to cut? Enter a number from 0-39: "))
        print(f"Cutting {cut} cards.")
        self.flip_card = self.deck[cut]
        print("\nFlip card:", self.flip_card)
        print("Hand:", self.player)
        print("Computer hand:", self.computer)  # DEBUGGING

    def peg(self):
        # While players have cards left, alternate placing one card at a time until total of 31.
        # Make copies of the hands so the originals are unaffected
        player_hand = self.player.copy()
        computer_hand = self.computer.copy()
        player_can_play = True
        computer_can_play = True
        continue_stack = True
        total = 0

        def computer_plays(hand, tot):
            card_index = randint(0, len(hand) - 1)
            card = hand[card_index]
            if card.value + tot <= 31:
                chosen_card = card
            else:
                chosen_card = hand[0]
            print("Opponent plays", chosen_card)
            self.table.append(hand.pop(card_index))
            tot += chosen_card.value
            print(self.table, "Sum =", tot)
            return hand, tot

        def player_plays(hand, tot):
            print("Available cards:", player_hand)
            while True:
                player_choice = int(input(f"Type card index (1 to {len(hand)}) to play: ")) - 1
                chosen_card = hand[player_choice]
                if chosen_card.value + tot > 31:
                    print("Total must not exceed 31. Try again.")
                else:
                    break
            self.table.append(hand.pop(player_choice))
            tot += chosen_card.value
            print("You play", chosen_card)
            print(self.table, "Sum =", tot)
            return hand, tot

        #def perform_check(p_hand, c_hand, tot):
        #    p_can_play = len(p_hand) and (p_hand[0].value + tot <= 31)
        #    c_can_play = len(c_hand) and (c_hand[0].value + tot <= 31)
        #    return p_can_play, c_can_play


        # Non dealer goes first
        print("\nLet the pegging begin!")
        if self.player_is_dealer:
            computer_hand, total = computer_plays(computer_hand, total)

        # Here's where it all goes down
        while len(player_hand) or len(computer_hand):  # while someone has cards left
            if player_can_play:
                player_hand, total = player_plays(player_hand, total)
            else:
                print("You cannot play.")
            player_can_play = len(player_hand) and (player_hand[0].value + total <= 31)
            computer_can_play = len(computer_hand) and (computer_hand[0].value + total <= 31)
            if total == 31 or (not player_can_play and not computer_can_play):
                print("End of stack!\n")
                #print(self.table, "Sum =", total, end="\n\n\n")
                self.table.clear()
                total = 0
                player_can_play = len(player_hand) and (player_hand[0].value + total <= 31)
                computer_can_play = len(computer_hand) and (computer_hand[0].value + total <= 31)
            if not len(player_hand) and not len(computer_hand):
                break
            if computer_can_play:
                computer_hand, total = computer_plays(computer_hand, total)
            else:
                print("Opponent cannot play.")

            player_can_play = len(player_hand) and (player_hand[0].value + total <= 31)
            computer_can_play = len(computer_hand) and (computer_hand[0].value + total <= 31)
            if total == 31 or (not player_can_play and not computer_can_play):
                print("End of stack!\n")
                #print(self.table, "Sum =", total, end="\n\n\n")
                self.table.clear()
                total = 0
                player_can_play = len(player_hand) and (player_hand[0].value + total <= 31)
                computer_can_play = len(computer_hand) and (computer_hand[0].value + total <= 31)
        print("Pegging completed!")

    def score(self):
        score = 0
        # 15 for 2
        # 15 for 4
        # pair for 6
        # 3-run for 9
        # 3-run for 12
        hand = [Card(5, 'H'), Card(7, 'D'), Card(7, 'H'), Card(8, 'D'), Card(9, 'D')]  # DEBUGGING
        # Use the powerset (n >= 2) of the list to find all card combos
        def powerset(s):
            return chain.from_iterable(combinations(s, r) for r in range(2, len(s) + 1))
        # Check the sum of each powerset. If it's 15, add +2 to the score.
        card_groups = list(powerset(hand))

        print(card_groups)  # DEBUGGING
        for group in card_groups:
            if sum(map(int, group)) == 15:  # finding fifteens
                score += 2
            if len(group) == 2 and group[0].rank == group[1].rank:  # finding pairs
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


def main():
    game = Cribbage()
    game.player_deals()
    game.peg()


if __name__ == '__main__':
    main()
