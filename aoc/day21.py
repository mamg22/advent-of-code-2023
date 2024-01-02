from collections import Counter, deque
from collections.abc import Sequence
from dataclasses import dataclass
from enum import Enum, auto
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
        if self is self.east:
            return Vector2d(1, 0)
        elif self is self.south:
            return Vector2d(0, 1)
        elif self is self.west:
            return Vector2d(-1, 0)
        elif self is self.north:
            return Vector2d(0, -1)
        else:
            raise ValueError("Invalid direction")



class Map:
    width: int
    height: int
    start: Vector2d
    rocks: set[Vector2d]
    reachable: set[Vector2d]

    def __init__(self: Self, width: int, height: int,
                 start: Vector2d, rocks: set[Vector2d], reachable: set[Vector2d]):
        self.width = width
        self.height = height
        self.start = start
        self.rocks = rocks
        self.reachable = reachable


def parse_input(data: Sequence[str]) -> Map:
    width = len(data[0])
    height = len(data)

    start: Vector2d = Vector2d(-1, -1)
    rocks: set[Vector2d] = set()

    for y, row in enumerate(data):
        for x, cell in enumerate(row):
            if cell == '#':
                rocks.add(Vector2d(x, y))
            elif cell == 'S':
                start = Vector2d(x, y)
    
    positions: list[Vector2d] = [start]
    seen: set[Vector2d] = set()
    reachable: set[Vector2d] = set()

    directions = [d.as_vector() for d in Direction]

    while positions:
        position = positions.pop()

        seen.add(position)

        for direction in directions:
            target = position + direction

            if target in seen:
                continue

            if target.x not in range(width) or target.y not in range(height):
                continue

            if target not in rocks:
                reachable.add(target)
                positions.append(target)
    
    
    return Map(width, height, start, rocks, reachable)


def manhattan_distance(origin: Vector2d, point: Vector2d):
    diff = point - origin
    return abs(diff.x) + abs(diff.y)


# Based on
# https://github.com/derailed-dash/Advent-of-Code/blob/master/src/AoC_2023/Dazbo's_Advent_of_Code_2023.ipynb

def count_reachable(world: Map, steps: int) -> int:
    tile = Vector2d(0, 0)

    queue: deque[tuple[Vector2d, Vector2d, int]] = deque()
    queue.append((tile, world.start, steps))

    seen: set[tuple[Vector2d, Vector2d]] = set()
    answer: set[tuple[Vector2d, Vector2d]] = set()
    tiles_for_steps = steps // world.width + 1

    directions = [d.as_vector() for d in Direction]

    while queue:
        tile, position, steps = queue.popleft()

        if steps >= 0:
            if steps % 2 == 0:
                answer.add((tile, position))
            
            if steps > 0:
                steps -= 1

                for dir_vector in directions:
                    neighbor = position + dir_vector

                    new_tile = tile

                    if neighbor.x not in range(world.width) or neighbor.y not in range(world.height):
                        new_tile = tile + dir_vector
                        neighbor = neighbor - (dir_vector * world.width)
                                        
                    if (new_tile, neighbor) in seen or neighbor in world.rocks:
                        continue

                    queue.append((new_tile, neighbor, steps))
                    seen.add((new_tile, neighbor))

    
    return len(answer)


def solve_part1(data: Sequence[str], steps: int) -> int:
    world = parse_input(data)

    return count_reachable(world, steps)


def quadratic_solve(world: Map, counts: Sequence[int], steps: int):
    c = counts[0]
    b = (4 * counts[1] - 3 * counts[0] - counts[2]) // 2
    a = counts[1] - counts[0] - b

    x = (steps - world.width // 2) // world.width
    return a * x ** 2 + b * x + c


def solve_part2(data: Sequence[str], steps: int) -> int:
    world = parse_input(data)

    counts = [count_reachable(world, 65 + i * 131) for i in range(3)]

    return quadratic_solve(world, counts, steps)

def main() -> None:
    with open("input/day21.txt", 'r') as data_file:
        data: list[str] = data_file.read().splitlines()

    print("Part 1:", solve_part1(data, 64))
    print("Part 2:", solve_part2(data, 26501365))


if __name__ == '__main__':
    main()
