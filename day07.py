from __future__ import annotations
from dataclasses import dataclass, field
from functools import cached_property
from textwrap import dedent
from typing import Iterator


@dataclass
class File:
    name: str
    size: int


@dataclass
class Directory:
    name: str
    children: dict[str, Directory | File] = field(default_factory=dict)

    @cached_property
    def size(self) -> int:
        return sum(child.size for child in self.children.values())

    def __getitem__(self, path: str | list[str]) -> Directory | File:
        if isinstance(path, str):
            return self.children[path]

        current = self
        for part in path:
            assert isinstance(current, Directory), f"'{current}' is not a directory"
            current = current.children[part]

        return current

    def walk(self) -> Iterator[Directory]:
        for child in self.children.values():
            if isinstance(child, Directory):
                yield child
                yield from child.walk()


def parse_terminal_output(contents: str) -> Directory:
    cwd_parts = []
    root = Directory("/")

    reading_output = False

    for line in contents.splitlines():
        match line.split():
            case ["$", "ls"]:
                reading_output = True

            case ["$", "cd", name]:
                match name:
                    case "/":
                        cwd_parts.clear()
                    case "..":
                        cwd_parts.pop()
                    case _:
                        cwd_parts.append(name)

            case [x, name] if reading_output:
                dir = root[cwd_parts]
                assert isinstance(dir, Directory)

                if x == "dir":
                    dir.children[name] = Directory(name)
                elif x.isnumeric():
                    dir.children[name] = File(name, size=int(x))

    return root


example = dedent(
    """
    $ cd /
    $ ls
    dir a
    14848514 b.txt
    8504156 c.dat
    dir d
    $ cd a
    $ ls
    dir e
    29116 f
    2557 g
    62596 h.lst
    $ cd e
    $ ls
    584 i
    $ cd ..
    $ cd ..
    $ cd d
    $ ls
    4060174 j
    8033020 d.log
    5626152 d.ext
    7214296 k
""".strip()
)

assert parse_terminal_output(example).size == 48_381_165


with open("input") as f:
    puzzle_input = f.read()

filesystem_root = parse_terminal_output(puzzle_input)

assert (
    sum(
        size
        for directory in filesystem_root.walk()
        if (size := directory.size) <= 100_000
    )
    == 1443806
)

total_disk_space = 70_000_000
required_unused_space = 30_000_000
current_unused_space = total_disk_space - filesystem_root.size
lacking_space = required_unused_space - current_unused_space

assert (
    min(
        size
        for directory in filesystem_root.walk()
        if (size := directory.size) >= lacking_space
    )
    == 942298
)
