from collections.abc import Sequence
from dataclasses import dataclass
from enum import Enum, auto
from itertools import pairwise
import re
from typing import Self


@dataclass(slots=True, order=True)
class Vector2d:
    x: int
    y: int

    def __add__(self, other: Self) -> Self:
        return self.__class__(self.x + other.x, self.y + other.y)
    
    def __sub__(self, other: Self) -> Self:
        return self.__class__(self.x - other.x, self.y - other.y)
    
    def __neg__(self) -> Self:
        return self.__class__(-self.x, -self.y)

    def __mul__(self, scalar: int):
        return self.__class__(self.x * scalar, self.y * scalar)

    def __repr__(self):
        return f"{self.__class__.__name__}({self.x}, {self.y})"
    
    def __hash__(self):
        return hash((self.x, self.y))


class Direction(Enum):
    east = auto()
    south = auto()
    west = auto()
    north = auto()

    @property
    def complement(self):
        match self:
            case self.east:
                return self.west
            case self.south:
                return self.north
            case self.west:
                return self.east
            case self.north:
                return self.south

    def as_vector(self):
        match self:
            case self.east:
                return Vector2d(1, 0)
            case self.south:
                return Vector2d(0, 1)
            case self.west:
                return Vector2d(-1, 0)
            case self.north:
                return Vector2d(0, -1)


@dataclass
class Instruction:
    direction: Direction
    length: int


def parse_simple_instruction(line: str) -> Instruction:
    direction_str, length_str, _ = line.split()

    match direction_str:
        case 'R':
            direction = Direction.east
        case 'D':
            direction = Direction.south
        case 'L':
            direction = Direction.west
        case 'U':
            direction = Direction.north
        case _:
            raise ValueError(f"Invalid direction '{direction_str}'")
    
    length = int(length_str)

    return Instruction(direction, length)


COLOR_MATCHER = re.compile('#([0-9a-f]{5})([0-9a-f])')

def parse_color_instruction(line: str):
    hex_color = COLOR_MATCHER.search(line)

    if not hex_color:
        raise ValueError("Color not found in line")

    length_str, direction_str = hex_color.groups()

    length = int(length_str, base=16)

    match direction_str:
        case '0':
            direction = Direction.east
        case '1':
            direction = Direction.south
        case '2':
            direction = Direction.west
        case '3':
            direction = Direction.north
        case _:
            raise ValueError(f"Invalid direction '{direction_str}'")

    return Instruction(direction, length)



def parse_instructions(data: Sequence[str], use_color: bool) -> list[Instruction]:
    if not use_color:
        return [parse_simple_instruction(line) for line in data]
    else:
        return [parse_color_instruction(line) for line in data]



def process_instructions(instructions: Sequence[Instruction]) -> list[Vector2d]:
    cursor: Vector2d = Vector2d(0, 0)
    polygon: list[Vector2d] = [cursor]

    for instruction in instructions:
        cursor += instruction.direction.as_vector() * instruction.length
        polygon.append(cursor)
    
    return polygon


def shoelace(polygon: Sequence[Vector2d]) -> float:
    area = 0
    for lhs, rhs in pairwise(reversed(polygon)):
        area += lhs.x * rhs.y - lhs.y * rhs.x
    
    return abs(area / 2)


def perimeter(instructions: Sequence[Instruction]) -> float:
    return sum(instruction.length for instruction in instructions)


def calculate_area(data: Sequence[str], use_color: bool) -> int:
    instructions = parse_instructions(data, use_color=use_color)
    polygon = process_instructions(instructions)
    inner_area = shoelace(polygon)
    perimeter_area = perimeter(instructions)

    area = inner_area + perimeter_area / 2 + 1
    
    return int(area)


def solve_part1(data: Sequence[str]) -> int:
    return calculate_area(data, use_color=False)


def solve_part2(data: Sequence[str]) -> int:
    return calculate_area(data, use_color=True)


def main() -> None:
    with open("input/day18.txt", 'r') as data_file:
        data: list[str] = data_file.read().splitlines()

    print("Part 1:", solve_part1(data))
    print("Part 2:", solve_part2(data))


if __name__ == '__main__':
    main()