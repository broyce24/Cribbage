"""
Ben Royce
This is a program to emulate the game of Cribbage.
"""
from Card import Card
from random import shuffle, randint
import time
from itertools import chain, combinations


class Cribbage:
    def __init__(self):
        self.cards = [Card(r, s) for s in "SCHD" for r in range(1, 14)]
        self.deck = self.cards.copy()
        shuffle(self.deck)
        self.player = []
        self.player_score = 0
        self.computer = []
        self.computer_score = 0
        self.crib = []
        self.table = []
        self.player_is_dealer = True
        self.flip_card = None

    def pick_first_dealer(self):
        while True:
            player_choice = self.deck[int(input("Pick a card from the deck! Type an index from 1-52: ")) - 1]
            computer_choice = self.deck[randint(1, 52)]
            print("The card you chose is", player_choice)
            print("The computer chose", computer_choice)
            if player_choice.rank == computer_choice.rank:
                print("It's a tie! Pick again.")
                continue
            return player_choice.rank < computer_choice.rank

    def deal(self, player_deals):
        """
        Deals cards based on the dealer.
        """
        # Dealing cards. Non-dealer gets first card.
        print("You are the dealer." if player_deals else "Computer is the dealer.")
        for i in range(12):
            j = i if player_deals else i + 1  # neat trick to flip parity
            if j % 2:
                self.computer.append(self.deck.pop(0))
            else:
                self.player.append(self.deck.pop(0))
        self.player.sort(key=lambda c: c.rank)
        self.computer.sort(key=lambda c: c.rank)

        # Contributing cards to crib
        target = "your" if player_deals else "Computer's"
        print(f"Choose two cards to contribute to {target} crib.")
        for i in range(2):
            print("Hand:", self.player)
            crib_card = int(input(f"Type card index (1 to {6 - i}) to contribute it: "))
            self.crib.append(self.player.pop(crib_card - 1))
            self.crib.append(self.computer.pop(randint(0, 6 - i - 1)))  # Computer randomly chooses crib cards
        print("Selection:", self.crib[::2])  # Shows only the player's contribution

        # Cutting the deck
        if player_deals:
            cut = randint(1, 39)
            print("Computer chooses", cut, "card" if cut == 1 else "cards", "to cut.")
        else:
            while True:  # this is just to catch numbers outside the cut range
                cut = int(input("How many cards would you like to cut? Enter a number from 1-39: "))
                if 1 <= cut <= 39:
                    break
            print("Cutting", cut, "card." if cut == 1 else "cards.")
        self.flip_card = self.deck[cut]

        # Printing information
        print("\nFlip card:", self.flip_card)
        print("Hand:", self.player)

    def peg(self):
        player_hand = self.player.copy()
        computer_hand = self.computer.copy()
        total = 0

        def play(player):
            nonlocal player_hand, computer_hand, total
            if player == 'computer':
                while True:  # Making sure we get a card that doesn't go over 31
                    card_index = randint(0, len(computer_hand) - 1)
                    card = computer_hand[card_index]
                    if card.value + total <= 31:
                        break
                self.table.append(computer_hand.pop(card_index))
                print("Computer plays", card)
                self.computer_score += get_table_score()
            else:
                while True:
                    print("Hand:", player_hand)
                    card_index = int(input(f"Type card index (1 to {len(player_hand)}) to play: ")) - 1
                    card = player_hand[card_index]
                    if card.value + total <= 31:
                        break
                self.table.append(player_hand.pop(card_index))
                print("You play", card)
                self.player_score += get_table_score()
            total += card.value
            print(self.table, "Sum =", total, end="\n\n")

        def get_table_score():
            score = 0
            cards_down = len(self.table)
            if cards_down == 1:
                return score

            if sum(map(int, self.table)) == 15:
                print("Fifteen! (+2)")
                score += 2

            elif sum(map(int, self.table)) == 31:
                print("Thirty one! (+2)")
                score += 2

            if self.table[-1].rank == self.table[-2].rank:
                if cards_down > 2 and self.table[-2].rank == self.table[-3].rank:
                    if cards_down > 3 and self.table[-3].rank == self.table[-4].rank:
                        print("Quads! (+4)")
                        score += 12
                    else:
                        print("Trips! (+3)")
                        score += 6
                else:
                    print("Pair! (+2)")
                    score += 2

            if cards_down > 2:
                for i in range(cards_down - 2):
                    if Cribbage.is_run(self.table[i:]):
                        run_length = cards_down - i
                        print(f"Run of {run_length}! (+{run_length})")
                        score += run_length
                        break
            return score

        # Non dealer goes first
        print("\nLet the pegging begin!")
        if self.player_is_dealer:
            play("computer")
        players_turn = True

        # PEGGING FINALLY GOT IT TO ALTERNATE IN A LOOP
        while len(player_hand) or len(computer_hand):  # while someone has cards left
            # time.sleep(1) debugging
            player_can_play = len(player_hand) and (player_hand[0].value + total <= 31)
            computer_can_play = len(computer_hand) and (computer_hand[0].value + total <= 31)
            if players_turn and player_can_play:
                play("player")
                players_turn = not computer_can_play
            elif computer_can_play:
                play("computer")
                players_turn = True
            else:
                print("End of stack!\n")
                self.table.clear()
                total = 0

        print("Pegging completed!")
        print("Computer's score:", self.computer_score)
        print("Player's score:", self.player_score)
        print()

    @staticmethod
    def is_run(cards):
        if isinstance(cards, list):
            cards.sort(key=lambda c: c.rank)
        for i in range(len(cards) - 1):
            if cards[i].rank - cards[i + 1].rank != -1:
                return False
        return True

    def scoring(self):

        def get_hand_score(hand):
            score = 0
            card_groups = reversed(list(chain.from_iterable(combinations(hand, r) for r in range(2, len(hand) + 1))))
            runs_of_4 = 0
            runs_of_5 = 0
            for group in card_groups:
                if sum(map(int, group)) == 15:
                    score += 2
                if len(group) == 5:
                    if len({card.suit for card in group}) == 1:
                        score += 5
                    if Cribbage.is_run(group):
                        score += 5
                        runs_of_5 += 1
                elif len(group) == 4:
                    if len({card.suit for card in group}) == 1:
                        score += 4
                    if runs_of_5 == 0 and Cribbage.is_run(group):
                        score += 4
                        runs_of_4 += 1
                elif len(group) == 3:
                    if runs_of_4 + runs_of_5 == 0 and Cribbage.is_run(group):
                        score += 3
                elif len(group) == 2:
                    if group[0].rank == group[1].rank:
                        score += 2
            return score

        full_hand_player = sorted(self.player + [self.flip_card], key=lambda c: c.rank)
        full_hand_computer = sorted(self.computer + [self.flip_card], key=lambda c: c.rank)
        full_hand_crib = sorted((self.crib + [self.flip_card]), key=lambda c: c.rank)
        player_score = get_hand_score(full_hand_player)
        computer_score = get_hand_score(full_hand_computer)
        crib_score = get_hand_score(full_hand_crib)
        if self.player_is_dealer:
            print("Computer's hand:", full_hand_computer)
            print("Computer's score:", computer_score)
            print("Your hand:", full_hand_player)
            print("Your score:", player_score)
            print("Your crib:", full_hand_crib)
            print("Crib score:", crib_score)
            self.computer_score += computer_score
            self.player_score += player_score + crib_score
        else:
            print("Your hand:", full_hand_player)
            print("Your score:", player_score)
            print("Computer's hand:", full_hand_computer)
            print("Computer's score:", computer_score)
            print("Computer's crib:", full_hand_crib)
            print("Crib score:", crib_score)
            self.player_score += player_score
            self.computer_score += computer_score + crib_score
        print()
        print("You have", self.player_score, "points.")
        print("Computer has", self.computer_score, "points.")
        print()
        self.player.clear()
        self.computer.clear()
        self.table.clear()
        self.crib.clear()
        self.deck = self.cards.copy()
        shuffle(self.deck)


def main():
    game = Cribbage()
    player_deals = game.pick_first_dealer()
    while True:
        game.deal(player_deals)
        game.peg()
        game.scoring()
        player_deals = not player_deals  # alternate dealer


if __name__ == "__main__":
    main()
