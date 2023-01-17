from copy import deepcopy
from dataclasses import dataclass
from itertools import count
import re
from typing import Iterator
from typing_extensions import Self


def parse_crate_stack_drawing(lines: Iterator[str]) -> dict[int, list[str]]:
    stacks = {}
    for i, line in enumerate(lines):
        if "[" not in line:
            break

        for j in count():
            if j * 4 >= len(line):
                break

            crate = line[j * 4 : (j + 1) * 4].strip("[ ]\n")
            if crate:
                stack = stacks.setdefault(j + 1, [])
                stack.append(crate)

    for stack in stacks.values():
        stack.reverse()

    assert next(lines).isspace()

    return stacks


@dataclass
class Rearrangement:
    amount: int
    source: int
    destination: int

    _PATTERN = re.compile(r"move (\d+) from (\d+) to (\d+)")

    @classmethod
    def parse(cls, s: str) -> Self:
        match_ = cls._PATTERN.match(s)
        assert match_ is not None

        amount, source, destination = (int(g) for g in match_.groups())
        return cls(amount, source, destination)


def parse_rearrangement_procedure(lines: Iterator[str]) -> list[Rearrangement]:
    return [Rearrangement.parse(line) for line in lines]


def simulate_rearrangement_procedure(
    stacks: dict[int, list[str]],
    procedure: list[Rearrangement],
    one_at_a_time: bool,
) -> dict[int, list[str]]:
    stacks = deepcopy(stacks)

    for rearrangement in procedure:
        amount = rearrangement.amount
        source = stacks[rearrangement.source]
        destination = stacks[rearrangement.destination]

        crates = source[-amount:]
        if one_at_a_time:
            crates.reverse()

        destination.extend(crates)

        for _ in range(amount):
            source.pop()

    return stacks


def tops(stacks: dict[int, list[str]]) -> str:
    return "".join(stack[-1] for _, stack in sorted(stacks.items()))


with open("input") as f:
    lines = iter(f.readlines())


stacks = parse_crate_stack_drawing(lines)
procedure = parse_rearrangement_procedure(lines)

assert (
    tops(simulate_rearrangement_procedure(stacks, procedure, one_at_a_time=True))
    == "HBTMTBSDC"
)
assert (
    tops(simulate_rearrangement_procedure(stacks, procedure, one_at_a_time=False))
    == "PQTJRSHWS"
)
