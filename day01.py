with open("input") as f:
    raw = f.read()

elfs = [
    [int(item) for item in items.splitlines()]
    for items in raw.split("\n\n")
]

calories = [sum(items) for items in elfs]

print(max(calories))

print(sum(sorted(calories)[-3:]))
