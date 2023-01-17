def find_marker(buffer: str, marker_length: int) -> int:
    for i, _ in enumerate(buffer):
        next_n = buffer[i : i + marker_length]
        all_different = len(set(next_n)) == marker_length
        if all_different:
            return i + marker_length

    return -1

assert find_marker("bvwbjplbgvbhsrlpgdmjqwftvncz", marker_length=4) == 5
assert find_marker("nppdvjthqldpwncqszvftbrmjlhg", marker_length=4) == 6
assert find_marker("nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg", marker_length=4) == 10
assert find_marker("zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw", marker_length=4) == 11

with open("input") as f:
    assert find_marker(f.read(), marker_length=4) == 1198


assert find_marker("mjqjpqmgbljsphdztnvjfqwrcgsmlb", marker_length=14) == 19
assert find_marker("bvwbjplbgvbhsrlpgdmjqwftvncz", marker_length=14) == 23
assert find_marker("nppdvjthqldpwncqszvftbrmjlhg", marker_length=14) == 23
assert find_marker("nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg", marker_length=14) == 29
assert find_marker("zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw", marker_length=14) == 26

with open("input") as f:
    assert find_marker(f.read(), marker_length=14) == 3120
