from Score import Score
class Player:
    def __init__(self, name):
        self.name = name
        self.score = Score()
        self.hand = []

    def get_points(self):
        return self.score.get_score()

    def choose_card(self, message, low, high):
        """
        Performs input validation when prompting the user to select a card.
        :param message: A string to be displayed to the user when asking for the card. Do not include a trailing space.
        :param low: The smallest valid index.
        :param high: The largest valid index.
        :return: A valid card index given by the user.
        """
        while True:
            index = input(message + f" Enter a number from {low} to {high}: ")
            try:
                index = int(index)
            except:
                print("Please enter an integer.")
                continue
            if not (low <= index <= high):
                print("Please enter a valid integer.")
                continue
            break
        return index

