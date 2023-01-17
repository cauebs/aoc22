from dataclasses import dataclass
from math import lcm, prod
from typing import Iterable, Literal, Mapping, NewType, Sequence


MonkeyId = NewType("MonkeyId", int)


@dataclass(frozen=True)
class Operation:
    operator: str
    operand: Literal["old"] | int

    def __call__(self, item: int) -> int:
        operand = item if self.operand == "old" else self.operand
        match self.operator:
            case "+":
                return item + operand
            case "*":
                return item * operand
            case _:
                raise Exception()


@dataclass(frozen=True)
class Test:
    divisor: int
    if_true: MonkeyId
    if_false: MonkeyId

    def __call__(self, item: int) -> MonkeyId:
        match item % self.divisor:
            case 0:
                return self.if_true
            case _:
                return self.if_false


@dataclass(frozen=True)
class Monkey:
    id: MonkeyId
    starting_items: Sequence[int]
    operation: Operation
    test: Test


def parse_monkey_id(line: str) -> MonkeyId:
    match line.rstrip(":").split():
        case "Monkey", number:
            return MonkeyId(int(number))
        case _:
            raise Exception(line)


def parse_starting_items(line: str) -> list[int]:
    match line.split():
        case "Starting", "items:", *numbers:
            return [int(n.rstrip(",")) for n in numbers]
        case _:
            raise Exception(line)


def parse_operation(line: str) -> Operation:
    match line.split():
        case "Operation:", "new", "=", "old", operator, "old":
            return Operation(operator, "old")
        case "Operation:", "new", "=", "old", operator, number:
            return Operation(operator, int(number))
        case _:
            raise Exception(line)


def parse_test(lines: tuple[str, str, str]) -> Test:
    match lines[0].split():
        case "Test:", "divisible", "by", number:
            divisor = int(number)
        case _:
            raise Exception(lines[0])

    match lines[1].split():
        case "If", "true:", "throw", "to", "monkey", number:
            if_true = MonkeyId(int(number))
        case _:
            raise Exception(lines[0])

    match lines[2].split():
        case "If", "false:", "throw", "to", "monkey", number:
            if_false = MonkeyId(int(number))
        case _:
            raise Exception(lines[0])

    return Test(divisor, if_true=if_true, if_false=if_false)


def parse_monkey(text: str) -> Monkey:
    lines = [line.strip() for line in text.splitlines()]

    monkey_id = parse_monkey_id(lines[0])
    items = parse_starting_items(lines[1])
    operation = parse_operation(lines[2])
    test = parse_test((lines[3], lines[4], lines[5]))

    return Monkey(monkey_id, items, operation, test)


def simulate(
    monkeys: Iterable[Monkey],
    rounds: int,
    relief: bool = True,
) -> dict[MonkeyId, int]:
    inspection_records = {monkey.id: 0 for monkey in monkeys}
    held_items = {monkey.id: list(monkey.starting_items) for monkey in monkeys}

    secret_relief_factor = lcm(*(monkey.test.divisor for monkey in monkeys))

    for _ in range(rounds):
        for monkey in monkeys:
            for item in held_items[monkey.id]:
                inspection_records[monkey.id] += 1
                item = monkey.operation(item)

                if relief:
                    item //= 3

                item %= secret_relief_factor

                target = monkey.test(item)
                held_items[target].append(item)

            held_items[monkey.id].clear()

    return inspection_records


def monkey_business_level(records: Mapping[MonkeyId, int]) -> int:
    two_most_active = sorted(records.values())[-2:]
    return prod(two_most_active)


with open("input") as f:
    monkeys = [parse_monkey(section) for section in f.read().split("\n\n")]


assert monkey_business_level(simulate(monkeys, rounds=20)) == 119715
assert (
    monkey_business_level(simulate(monkeys, rounds=10_000, relief=False)) == 18085004878
)
