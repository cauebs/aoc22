from enum import Enum


class Shape(Enum):
    ROCK = 0
    PAPER = 1
    SCISSORS = 2

    @property
    def score(self) -> int:
        return self.value + 1


class Result(Enum):
    LOSE = 0
    DRAW = 3
    WIN = 6

    @property
    def score(self) -> int:
        return self.value


def play(me: Shape, opponent: Shape) -> Result:
    match (opponent.value - me.value) % 3:
        case 0: return Result.DRAW
        case 1: return Result.LOSE
        case 2: return Result.WIN
        case _: assert False

def score(me: Shape, opponent: Shape) -> int:
    return play(me=me, opponent=opponent).score + me.score


def decide_move(expected_result: Result, opponent: Shape) -> Shape:
    match expected_result:
        case Result.DRAW: return opponent
        case Result.LOSE: return Shape((opponent.value - 1) % 3)
        case Result.WIN: return Shape((opponent.value + 1) % 3)



OPPONENT_MOVE = {
    "A": Shape.ROCK,
    "B": Shape.PAPER,
    "C": Shape.SCISSORS,
}


def decypher_guessed(rounds: list[list[str]]) -> list[tuple[Shape, Shape]]:
    """
    Part 1.
    """
    my_move = {
        "X": Shape.ROCK,
        "Y": Shape.PAPER,
        "Z": Shape.SCISSORS,
    }

    return [
        (my_move[r], OPPONENT_MOVE[l])
        for l, r in rounds
    ]


def decypher_correct(rounds: list[list[str]]) -> list[tuple[Result, Shape]]:
    """
    Part 2.
    """
    expected_result = {
        "X": Result.LOSE,
        "Y": Result.DRAW,
        "Z": Result.WIN,
    }

    return [
        (expected_result[r], OPPONENT_MOVE[l])
        for l, r in rounds
    ]


with open("input") as f:
    encrypted_strategy_guide = [
        line.split()
        for line in f.readlines()
    ]

assert sum(
    score(me=me, opponent=opponent)
    for me, opponent in decypher_guessed(encrypted_strategy_guide)
) == 11063

assert sum(
    score(me=decide_move(expected_result, opponent), opponent=opponent)
    for expected_result, opponent in decypher_correct(encrypted_strategy_guide)
) == 10349
