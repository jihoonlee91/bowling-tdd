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


def test_perfect_game_scores_300():
    game = Game()
    for _ in range(12):
        game.roll(10)

    assert game.score() == 300


def test_tenth_frame_spare_scores_bonus():
    game = Game()
    for _ in range(18):
        game.roll(0)
    game.roll(5)
    game.roll(5)
    game.roll(3)

    assert game.score() == 13


def test_consecutive_strikes_across_frames():
    game = Game()
    game.roll(10)
    game.roll(10)
    game.roll(5)
    game.roll(3)
    for _ in range(14):
        game.roll(0)

    assert game.score() == 51


def test_turkey_then_open_frame():
    game = Game()
    for _ in range(14):
        game.roll(0)
    game.roll(10)
    game.roll(10)
    game.roll(10)
    game.roll(4)
    game.roll(2)

    assert game.score() == 70
