from string import ascii_letters


def find_separated_item(rucksack: str) -> str:
    n = len(rucksack)
    assert n % 2 == 0
    first_compartment = rucksack[:n//2]
    second_compartment = rucksack[n//2:]

    in_both = set(first_compartment) & set(second_compartment)
    assert len(in_both) == 1
    return in_both.pop()


def priority(item: str) -> int:
    return ascii_letters.index(item) + 1


def groups(rucksacks: list[str], group_size: int = 3) -> list[list[str]]:
    assert len(rucksacks) % group_size == 0
    iterators = [iter(rucksacks)] * group_size
    return [list(group) for group in zip(*iterators)]


def find_badge(group: list[str]) -> str:
    rucksacks = (set(rucksack) for rucksack in group)
    in_common = set.intersection(*rucksacks)
    assert len(in_common) == 1
    return in_common.pop()


with open("input") as f:
    rucksacks = f.read().splitlines()


assert sum(priority(find_separated_item(rucksack)) for rucksack in rucksacks) == 8240
assert sum(priority(find_badge(group)) for group in groups(rucksacks)) == 2587
