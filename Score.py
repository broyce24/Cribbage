class Score:
    def __init__(self, player):
        self.value = 0
        self.max = 10
        self.player = player

    def get_score(self):
        return self.value

    def set_score(self, value):
        if value > self.value:
            print("Score incremented!")
            self.value = value
        if value >= self.max:
            print(f"{self.player} WINS!")

    score = property(get_score, set_score)