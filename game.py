class Game:
    MAX_PINS = 10
    NUM_FRAMES = 10

    def __init__(self):
        self.rolls = []

    def roll(self, pins):
        self.rolls.append(pins)

    def score(self):
        total = 0
        roll_index = 0
        for _ in range(self.NUM_FRAMES):
            if self._is_strike(roll_index):
                total += self.MAX_PINS + self._strike_bonus(roll_index)
                roll_index += 1
            elif self._is_spare(roll_index):
                total += self.MAX_PINS + self._spare_bonus(roll_index)
                roll_index += 2
            else:
                total += self._frame_total(roll_index)
                roll_index += 2
        return total

    def _is_strike(self, roll_index):
        return self.rolls[roll_index] == self.MAX_PINS

    def _is_spare(self, roll_index):
        return self._frame_total(roll_index) == self.MAX_PINS

    def _frame_total(self, roll_index):
        return self.rolls[roll_index] + self.rolls[roll_index + 1]

    def _strike_bonus(self, roll_index):
        return self.rolls[roll_index + 1] + self.rolls[roll_index + 2]

    def _spare_bonus(self, roll_index):
        return self.rolls[roll_index + 2]
