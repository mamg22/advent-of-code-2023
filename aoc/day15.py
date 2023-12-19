from collections import defaultdict
from dataclasses import dataclass
from typing import Self

def HASH(values: str) -> int:
    state = 0
    for value in values:
        value = ord(value)
        state = ((state + value) * 17) % 256
    
    return state

    
def extract_steps(data: list[str]) -> list[str]:
    return data[0].split(',')


def solve_part1(data: list[str]) -> int:
    sequence = extract_steps(data)

    return sum(HASH(s) for s in sequence)

@dataclass
class Step:
    def __init__(self: Self, step_str: str) -> Self:
        if '=' in step_str:
            label, focal_length = step_str.split('=')
            self.label = label
            self.hash = HASH(label)
            self.operation = '='
            self.focal_length = int(focal_length)
        else:
            label = step_str.removesuffix('-')
            self.label = label
            self.hash = HASH(label)
            self.operation = '-'
    
    def __repr__(self) -> str:
        return f"Step({self.label}{self.operation}{getattr(self, 'focal_length', '')})"


def calculate_focusing_power(hashmap: dict[int, dict[str, int]]) -> int:
    total = 0

    for box, slots in hashmap.items():
        for slot_number, focal_length in enumerate(slots.values(), 1):
            total += (box + 1) * slot_number * focal_length

    return total

def solve_part2(data: list[str]) -> int:
    sequence = [Step(step) for step in extract_steps(data)]

    hashmap = defaultdict(dict)

    for step in sequence:
        if step.operation == '=':
            hashmap[step.hash][step.label] = step.focal_length
        elif step.operation == '-' and step.label in hashmap[step.hash]:
            del hashmap[step.hash][step.label]
    
    return calculate_focusing_power(hashmap)

def main() -> None:
    with open("input/day15.txt", 'r') as data_file:
        data: list[str] = data_file.read().splitlines()

    print("Part 1:", solve_part1(data))
    print("Part 2:", solve_part2(data))


if __name__ == '__main__':
    main()