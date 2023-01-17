def parse_sections(interval_description: str) -> set[int]:
    low, high = interval_description.split("-")
    sections = range(int(low), int(high) + 1)
    return set(sections)


with open("input") as f:
    interval_pairs = [line.strip().split(",") for line in f.readlines()]

pairs = [(parse_sections(a), parse_sections(b)) for a, b in interval_pairs]

with_complete_overlap = [(a, b) for a, b in pairs if a.issubset(b) or b.issubset(a)]
assert len(with_complete_overlap) == 576

with_partial_overlap = [(a, b) for a, b in pairs if not a.isdisjoint(b)]
assert len(with_partial_overlap) == 905
