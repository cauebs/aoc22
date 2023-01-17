with open("input") as f:
    lines = f.read().splitlines()


def emulate(instructions: list[str]) -> list[int]:
    register_history = [1]

    for instruction in instructions:
        x = register_history[-1]
        match instruction.split():
            case ["noop"]:
                register_history.append(x)
            case ["addx", v]:
                register_history.append(x)
                register_history.append(x + int(v))

    return register_history


DISPLAY_WIDTH = 40
DISPLAY_HEIGHT = 9


def render(register_values: list[int]) -> str:
    output = ""

    for completed_cycles, register_value in enumerate(register_values):
        y = completed_cycles // DISPLAY_WIDTH
        x = completed_cycles % DISPLAY_WIDTH

        if abs(register_value - x) <= 1:
            output += "#"
        else:
            output += "."

        if x == DISPLAY_WIDTH - 1:
            if y == DISPLAY_HEIGHT - 1:
                break

            output += "\n"

    return output


register_values = emulate(lines)

signal_strengths = [
    ongoing_cycle * register_value
    for ongoing_cycle, register_value in enumerate(register_values, start=1)
]

assert sum(signal_strengths[19::40]) == 11820
print(render(register_values))
