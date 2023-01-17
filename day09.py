from __future__ import annotations
from dataclasses import dataclass
from math import hypot
from typing import NamedTuple


class Vec2D(NamedTuple):
    x: int = 0
    y: int = 0

    def __add__(self, other: Vec2D) -> Vec2D:
        return Vec2D(x=self.x + other.x, y=self.y + other.y)

    def __sub__(self, other: Vec2D) -> Vec2D:
        return Vec2D(x=self.x - other.x, y=self.y - other.y)

    def magnitude(self) -> float:
        return hypot(*self)

    def to_unit(self) -> Vec2D:
        return Vec2D(
            x=self.x // abs(self.x or 1),
            y=self.y // abs(self.y or 1),
        )


@dataclass
class Motion:
    direction: Vec2D
    steps: int


def parse_motion(s: str) -> Motion:
    a, b = s.split()

    direction = {
        "R": Vec2D(x=-1),
        "D": Vec2D(y=-1),
        "L": Vec2D(x=1),
        "U": Vec2D(y=1),
    }[a]
    steps = int(b)

    return Motion(direction, steps)


def read_motions(s: str) -> list[Motion]:
    return [parse_motion(line) for line in s.splitlines()]


def simulate_rope_tail_positions(motions: list[Motion], n_knots: int) -> set[Vec2D]:
    knots = [Vec2D()] * n_knots
    visited_by_tail = {knots[-1]}

    for motion in motions:
        for _ in range(motion.steps):
            knots[0] += motion.direction

            for i, _ in enumerate(knots[1:], start=1):
                delta = knots[i - 1] - knots[i]
                if delta.magnitude() >= 2:
                    knots[i] += delta.to_unit()

            visited_by_tail.add(knots[-1])

    return visited_by_tail


with open("input") as f:
    motions = read_motions(f.read())

assert len(simulate_rope_tail_positions(motions, n_knots=2)) == 6030
assert len(simulate_rope_tail_positions(motions, n_knots=10)) == 2545
