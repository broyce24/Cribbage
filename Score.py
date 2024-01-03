class Score:

    max_score = 10
    def __init__(self):
        self.value = 0

    def getter(self):
        return self.value

    def setter(self, value):
        if value > self.value:
            print("Score incremented!")
            self.value = value
        if value >= self.max:
            print(f"{self.player} WINS!")

    def __iadd__(self, other):
        if self.value + other >= Score.max_score:
            print("YOU WIN!")
            self.value += other
            return self

        self.value += other
        return self

    score = property(get_score, set_score)
