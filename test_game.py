from game import Game


def test_all_gutters_scores_zero():
    game = Game()
    for _ in range(20):
        game.roll(0)

    assert game.score() == 0


def test_all_ones_scores_twenty():
    game = Game()
    for _ in range(20):
        game.roll(1)

    assert game.score() == 20


def test_one_spare_scores_bonus():
    game = Game()
    game.roll(5)
    game.roll(5)
    game.roll(3)
    for _ in range(17):
        game.roll(0)

    assert game.score() == 16


def test_one_strike_scores_bonus():
    game = Game()
    game.roll(10)
    game.roll(3)
    game.roll(4)
    for _ in range(16):
        game.roll(0)

    assert game.score() == 24
