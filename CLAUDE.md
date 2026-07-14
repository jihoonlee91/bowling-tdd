# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project

Bowling Game Kata, implemented in Python using TDD (test first, then implementation).
The repo starts empty except for scaffolding — `game.py` (the `Game` class) does not
exist yet and should be created incrementally as tests are written for it.

## Commands

```bash
# create/activate a virtualenv (first time only)
python -m venv .venv
.venv\Scripts\activate        # PowerShell: .venv\Scripts\Activate.ps1

# install dev dependencies
pip install -r requirements-dev.txt

# run the full test suite
pytest

# run a single test file / test case
pytest test_game.py
pytest test_game.py::test_all_gutters_scores_zero -v
```

## Scope of the kata

The `Game` class exposes exactly two methods:

- `roll(pins: int) -> None` — called once per ball thrown.
- `score() -> int` — returns the total score once a full game has been rolled.

Per the kata rules, the implementation does **not** need to validate:
- that individual rolls are legal (e.g. `pins` in range, frame total ≤ 10),
- that the number of rolls/frames recorded is well-formed,
- mid-game/intermediate frame scores (only the final total via `score()` matters).

## Scoring rules (must be encoded correctly in `score()`)

A game has 10 frames. Each frame is normally 2 rolls, scored as pins knocked down
plus bonuses:

- **Spare** (two rolls in a frame total 10): frame score = 10 + pins on the *next
  one* roll.
- **Strike** (first roll in a frame is 10): frame ends after one roll; frame score
  = 10 + pins on the *next two* rolls.
- **10th frame**: if it's a spare or strike, the player gets one or two extra
  fill balls respectively, so the 10th frame can have up to 3 rolls total. These
  fill balls count only toward completing the 10th frame's bonus — there is no
  11th frame.

Because strike/spare bonuses look ahead into rolls that may belong to later
frames (or fill balls in frame 10), the natural implementation keeps a flat list
of all rolls as recorded by `roll()` and computes `score()` by walking that list
frame-by-frame, rather than trying to track frame boundaries during `roll()`.
