# Bowling Game Kata (TDD)

볼링 게임 점수 계산기를 **Agentic TDD**(Plan → RED → GREEN → REFACTOR, 매 단계 Human-in-the-Loop 승인)로 구현한 카타입니다.

## 목차

- [요구사항](#요구사항)
- [파일 구성](#파일-구성)
- [실행 방법](#실행-방법)
- [구현](#구현)
- [테스트 목록](#테스트-목록)
- [Agentic TDD 진행 방식](#agentic-tdd-진행-방식)
- [커밋 히스토리로 확인하기](#커밋-히스토리로-확인하기)

## 요구사항

`Game` 클래스는 메서드 두 개만 노출합니다.

- `roll(pins: int) -> None` — 한 번 굴릴 때마다 호출
- `score() -> int` — 한 게임(10프레임)이 끝난 뒤 총점 반환

스코어링 규칙:

- **스페어**(한 프레임 두 롤 합 10) = 10 + 다음 1롤
- **스트라이크**(첫 롤이 10) = 10 + 다음 2롤
- **10프레임**은 스페어/스트라이크 시 필 볼(fill ball)로 최대 3롤까지 허용하되, 11프레임은 없음

개별 롤/프레임의 유효성(핀 개수 범위, 프레임 합계 등)은 검증하지 않습니다. (kata 범위 밖)

## 파일 구성

```
.
├── game.py                                 # Game 클래스 구현 (프로덕션 코드)
├── test_game.py                            # pytest 테스트 8개
├── Plan.md                                 # 요구사항 → 테스트 케이스 분해 계획, 사이클별 근거
├── README.md                               # 이 문서
├── CLAUDE.md                               # 프로젝트 규칙 (Claude Code용)
├── pyproject.toml                          # pytest 설정
├── requirements-dev.txt                    # 개발 의존성 (pytest)
└── .claude/skills/test-driven-development/
    ├── SKILL.md                            # TDD + Human-in-the-Loop 규칙
    └── testing-anti-patterns.md            # 테스트 안티패턴 레퍼런스
```

## 실행 방법

```bash
pip install -r requirements-dev.txt
pytest -v
```

Python 3.10 이상이 필요합니다 (`pyproject.toml` 참고).

## 구현

`game.py` 전체:

```python
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
```

**동작 방식**: `roll()`은 굴린 핀 수를 `self.rolls` 리스트에 그대로 쌓기만 한다. `score()`가 이 평평한 리스트를 10프레임만큼 순회하며, 각 프레임 시작 위치(`roll_index`)에서 스트라이크인지·스페어인지 판별해 보너스를 더하고 다음 프레임 시작 위치로 넘어간다(스트라이크면 +1, 아니면 +2). 프레임 도중 상태를 별도로 추적하지 않기 때문에 스트라이크·스페어 보너스가 프레임 경계를 넘나들거나 10프레임의 필 볼을 가리키는 경우도 같은 로직으로 자연스럽게 처리된다.

## 테스트 목록

`Plan.md`에서 요구사항을 점진적으로 분해한 순서 그대로 작성되었습니다. 단순한 케이스부터 시작해 각 테스트가 이전 테스트로는 검증되지 않는 새로운 규칙만 다루도록 설계했습니다.

| # | 테스트 | 검증 내용 | GREEN 단계 |
|---|---|---|---|
| 1 | `test_all_gutters_scores_zero` | 전부 거터 → 0점 | 코드 작성 (`score()` 하드코딩 0) |
| 2 | `test_all_ones_scores_twenty` | 보너스 없는 단순 합산 | 코드 작성 (`rolls` 합산) |
| 3 | `test_one_spare_scores_bonus` | 스페어 보너스(다음 1롤) | 코드 작성 (프레임 워크 도입) |
| 4 | `test_one_strike_scores_bonus` | 스트라이크 보너스(다음 2롤) | 코드 작성 (스트라이크 분기 추가) |
| 5 | `test_perfect_game_scores_300` | 10프레임 경계 + 필 볼이 별도 프레임을 만들지 않음 | **없음** (기존 로직이 이미 커버) |
| 6 | `test_tenth_frame_spare_scores_bonus` | 10프레임에 한정된 스페어 + 필 볼 1개 | **없음** |
| 7 | `test_consecutive_strikes_across_frames` | 스트라이크 보너스가 프레임 경계를 넘어 겹치는 경우 | **없음** |
| 8 | `test_turkey_then_open_frame` | 연속 3스트라이크(터키) 뒤 10프레임 필 볼 2개로 마무리 | **없음** |

5~8번은 3~4번 사이클에서 일반화된 프레임 워크 로직이 이미 커버하고 있어 GREEN 단계(코드 변경) 없이 즉시 통과했다. 이는 사후 테스트(test-after)와는 다르다 — 테스트를 먼저 작성하고 실행해서 "우연히 이미 맞는 동작"임을 확인한 것이며, 회귀를 막아주는 유효한 테스트로 판단해 그대로 유지했다.

```bash
pytest -v
# 8 passed
```

## Agentic TDD 진행 방식

이 저장소는 [`.claude/skills/test-driven-development/SKILL.md`](.claude/skills/test-driven-development/SKILL.md)의 TDD Skill을 기반으로, 다음 체크포인트마다 사람의 승인을 받은 뒤에만 다음 단계로 진행했다.

```
PLAN 승인 → RED 승인 → GREEN 승인 → REFACTOR 승인
```

| 체크포인트 | 산출물 | 사람이 확인하는 것 |
|---|---|---|
| PLAN | `Plan.md` (테스트 케이스 목록 + 근거) | 요구사항을 빠짐없이 커버하는가, 불필요한 케이스는 없는가 |
| RED | 실패하는 테스트 코드 | Plan과 정확히 일치하는가, 올바른 이유로 실패하는가 |
| GREEN | 테스트를 통과시키는 최소 코드 | 과도한 일반화·불필요한 기능이 섞이지 않았는가 |
| REFACTOR | 정리된 코드 (동작 동일) | 여전히 전체 테스트가 그린인가 |

커밋도 단계별로 분리했다:

- **RED 커밋**: 그 사이클의 테스트(+ 갱신된 `Plan.md`)만 커밋
- **REVIEW/GREEN 커밋**: 최소 구현을 사람이 검토한 뒤 별도 커밋 — 코드 변경 없이 테스트만 통과했다면 그 사실을 커밋 메시지에 남기고 억지로 GREEN 커밋을 만들지 않음
- **REFACTOR 커밋**: 전체 테스트가 그린인 상태에서만, 동작 변경 없는 정리만 커밋

이렇게 분리하면 git 히스토리만 보고도 "테스트가 먼저 실패했는가 → 그다음 최소 코드가 추가됐는가"를 검증할 수 있다.

## 커밋 히스토리로 확인하기

```bash
git log --oneline
```

각 커밋 메시지가 `RED N`, `GREEN N`/`REVIEW N`, `REFACTOR` 단계를 명시하고 있어, 커밋 로그만 훑어봐도 이 카타가 실제로 테스트 우선으로 진행됐는지 감사(audit)할 수 있다.
