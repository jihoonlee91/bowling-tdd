# Bowling Game Kata (TDD)

볼링 게임 점수 계산기를 **Agentic TDD**(Plan → RED → GREEN → REFACTOR, 매 단계 Human-in-the-Loop 승인)로 구현한 카타입니다.

## 요구사항

`Game` 클래스는 메서드 두 개만 노출합니다.

- `roll(pins: int) -> None` — 한 번 굴릴 때마다 호출
- `score() -> int` — 한 게임(10프레임)이 끝난 뒤 총점 반환

스코어링 규칙:

- **스페어**(한 프레임 두 롤 합 10) = 10 + 다음 1롤
- **스트라이크**(첫 롤이 10) = 10 + 다음 2롤
- **10프레임**은 스페어/스트라이크 시 필 볼(fill ball)로 최대 3롤까지 허용하되, 11프레임은 없음

개별 롤/프레임의 유효성(핀 개수 범위 등)은 검증하지 않습니다.

## 실행 방법

```bash
pip install -r requirements-dev.txt
pytest -v
```

## 구현

```python
# game.py
class Game:
    def __init__(self):
        self.rolls = []

    def roll(self, pins):
        self.rolls.append(pins)

    def score(self):
        total = 0
        roll_index = 0
        for _ in range(10):
            if self.rolls[roll_index] == 10:
                total += 10 + self.rolls[roll_index + 1] + self.rolls[roll_index + 2]
                roll_index += 1
            else:
                first, second = self.rolls[roll_index], self.rolls[roll_index + 1]
                if first + second == 10:
                    total += 10 + self.rolls[roll_index + 2]
                else:
                    total += first + second
                roll_index += 2
        return total
```

굴린 롤을 평평한 리스트로 쌓아두고, `score()`가 프레임 경계를 따라 순회하며 스트라이크/스페어 보너스를 계산합니다. 프레임 도중에 상태를 추적하지 않기 때문에 스트라이크로 프레임 폭이 줄어드는 경우도 자연스럽게 처리됩니다.

## 테스트 목록

`Plan.md`에서 요구사항을 점진적으로 분해한 순서 그대로 작성되었습니다. 단순한 케이스부터 시작해 각 테스트가 이전 테스트로는 검증되지 않는 새로운 규칙만 다루도록 설계했습니다.

| # | 테스트 | 검증 내용 |
|---|---|---|
| 1 | `test_all_gutters_scores_zero` | 전부 거터 → 0점 |
| 2 | `test_all_ones_scores_twenty` | 보너스 없는 단순 합산 |
| 3 | `test_one_spare_scores_bonus` | 스페어 보너스(다음 1롤) |
| 4 | `test_one_strike_scores_bonus` | 스트라이크 보너스(다음 2롤) |
| 5 | `test_perfect_game_scores_300` | 10프레임 경계 + 필 볼이 별도 프레임을 만들지 않음 |
| 6 | `test_tenth_frame_spare_scores_bonus` | 10프레임에 한정된 스페어 + 필 볼 1개 |
| 7 | `test_consecutive_strikes_across_frames` | 스트라이크 보너스가 프레임 경계를 넘어 겹치는 경우 |
| 8 | `test_turkey_then_open_frame` | 연속 3스트라이크(터키) 뒤 10프레임 필 볼 2개로 마무리 |

5~8번은 3~4번 사이클에서 일반화된 프레임 워크 로직이 이미 커버하고 있어 **GREEN 단계(코드 변경) 없이 즉시 통과**했습니다. 커밋 로그에 그 사실을 그대로 남겨두었습니다.

```bash
pytest -v
# 8 passed
```

## Agentic TDD 진행 방식

이 저장소는 `.claude/skills/test-driven-development/`에 있는 TDD Skill을 기반으로, 다음 체크포인트마다 사람의 승인을 받은 뒤에만 다음 단계로 진행했습니다.

```
PLAN 승인 → RED 승인 → GREEN 승인 → REFACTOR 승인
```

- **Plan.md**: 요구사항을 테스트 케이스 목록으로 먼저 분해하고 사람이 검토
- **RED 커밋**: 그 사이클의 테스트(+ 갱신된 Plan.md)만 커밋
- **REVIEW/GREEN 커밋**: 최소 구현을 사람이 검토("과도한 일반화 없는가")한 뒤 별도 커밋
  - 테스트가 코드 변경 없이 바로 통과한 경우, 그 사실을 커밋 메시지에 명시하고 억지로 GREEN 커밋을 만들지 않음
- 커밋을 RED/GREEN 단계로 분리해, git 히스토리만으로도 "테스트가 먼저 실패했는가 → 그다음 최소 코드가 추가됐는가"를 검증할 수 있도록 함

자세한 규칙은 [`.claude/skills/test-driven-development/SKILL.md`](.claude/skills/test-driven-development/SKILL.md)를 참고하세요.
