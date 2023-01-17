from itertools import count
import math
from textwrap import dedent


def parse_height_map(raw: str) -> list[list[int]]:
    return [[int(c) for c in line] for line in raw.splitlines()]


def is_tree_visible(height_map: list[list[int]], row: int, column: int) -> bool:
    n_rows = len(height_map)
    n_columns = len(height_map[0])

    tree = height_map[row][column]

    if all(height_map[row][j] < tree for j in range(column)):
        return True

    if all(height_map[row][j] < tree for j in range(column + 1, n_columns)):
        return True

    if all(height_map[i][column] < tree for i in range(row)):
        return True

    if all(height_map[i][column] < tree for i in range(row + 1, n_rows)):
        return True

    return False


def count_visible_trees(height_map: list[list[int]]) -> int:
    return sum(
        is_tree_visible(height_map, row=i, column=j)
        for i, row in enumerate(height_map)
        for j, _ in enumerate(row)
    )


def viewing_distance(
    height_map: list[list[int]],
    row: int,
    column: int,
    direction_vector: tuple[int, int],
) -> int:
    delta_x, delta_y = direction_vector
    tree = height_map[row][column]

    for distance in count(start=1):
        try:
            other_row = row + delta_y * distance
            other_column = column + delta_x * distance
            if other_row < 0 or other_column < 0:
                raise IndexError()
            other_tree = height_map[other_row][other_column]

        except IndexError:
            return distance - 1

        if other_tree >= tree:
            return distance

    assert False


def scenic_score(height_map: list[list[int]], row: int, column: int) -> int:
    return math.prod(
        [
            viewing_distance(height_map, row, column, (0, -1)),
            viewing_distance(height_map, row, column, (0, 1)),
            viewing_distance(height_map, row, column, (-1, 0)),
            viewing_distance(height_map, row, column, (1, 0)),
        ]
    )


raw_example_map = dedent(
    """
    30373
    25512
    65332
    33549
    35390
    """
).strip()
example_map = parse_height_map(raw_example_map)

assert count_visible_trees(example_map) == 21
assert scenic_score(example_map, 1, 2) == 4
assert scenic_score(example_map, 3, 2) == 8


with open("input") as f:
    height_map = parse_height_map(f.read())

assert count_visible_trees(height_map) == 1719
assert (
    max(
        scenic_score(height_map, i, j)
        for i, row in enumerate(height_map)
        for j, _ in enumerate(row)
    )
    == 590824
)
