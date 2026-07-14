from game import Game


def test_all_gutters_scores_zero():
    game = Game()
    for _ in range(20):
        game.roll(0)

    assert game.score() == 0
