from enum import Enum, auto
from dataclasses import dataclass
from typing import Any, Optional
from itertools import cycle
from functools import cache


class Grid:
    def __init__(self, 
                 width: Optional[int] = None, height: Optional[int] = None,
                 default_value: Any = None, 
                 content: Optional[list[list[Any]]] = None):
        if content is not None:
            self.width = max(map(len, content))
            self.height = len(content)
            self.content = content.copy()
        else:
            if width is None or height is None:
                raise ValueError("Grid width or height cannot be None unless content is provided")
            
            self.width = width
            self.height = height
            self.content = [[default_value] * width for _ in range(height)]

    
    def get(self, x: int, y: int):
        # if x < 0 or x > self.width or y < 0 or y > self.height:
        #     raise IndexError(f"({x}, {y}) is out of grid area")
        return self.content[y][x]

    def set(self, x: int, y: int, value: Any):
        # if x < 0 or x > self.width or y < 0 or y > self.height:
        #     raise IndexError(f"({x}, {y}) is out of grid area")
        self.content[y][x] = value

    def __hash__(self):
        return hash(''.join([''.join(x) for x in self.content]))

    @property
    def rows(self):
        yield from self.content
    
    @property
    def columns(self):
        for x in range(self.width):
            yield [self.content[y][x] for y in range(self.height)]


@dataclass(slots=True)
class Vector2d:
    x: int
    y: int

    def __add__(self, other: 'Vector2d'):
        return Vector2d(self.x + other.x, self.y + other.y)
    
    def __sub__(self, other: 'Vector2d'):
        return Vector2d(self.x - other.x, self.y - other.y)

    def rotated(self, counter_clockwise: bool = False):
        if counter_clockwise:
            return Vector2d(self.y * -1, self.x)
        else:
            return Vector2d(self.y, self.x * -1)


Rock = str

# class Rock(Enum):
#     none = '.'
#     square = '#'
#     round = 'O'

#     def __repr__(self) -> str:
#         return self.value

class Direction(Enum):
    east = auto()
    south = auto()
    west = auto()
    north = auto()


def extract_info(data: list[str]):
    grid = Grid(len(data[0]), len(data), '.')

    for y, line in enumerate(data):
        for x, cell in enumerate(line):
            grid.content[y][x] = cell
    
    return grid


@cache
def slide_rocks(line: tuple[Rock], backwards: bool) -> list[Rock]:
    result: list[Rock] = []
    insertion_point = 0

    expect_n_rocks = line.count('O')
    n_rocks = 0

    if not backwards:
        for n, rock in enumerate(line):
            if rock == '.':
                result.insert(insertion_point, rock)
            elif rock == 'O':
                n_rocks += 1
                result.append(rock)
            elif rock == '#':
                result.append(rock)
                insertion_point = n + 1
    else:
        for n, rock in enumerate(line):
            if rock == '.':
                result.append(rock)
            elif rock == 'O':
                n_rocks += 1
                result.insert(insertion_point, rock)
            elif rock == '#':
                result.append(rock)
                insertion_point = n + 1
    
    assert n_rocks == expect_n_rocks
    
    return result

@cache
def tilt(grid: Grid, direction: Direction) -> Grid:
    result = Grid(content=grid.content.copy())
    match direction:
        case Direction.east | Direction.west:
            for y, row in enumerate(grid.rows):
                new_row = slide_rocks(tuple(row), backwards=(direction == Direction.west))

                for x, rock in enumerate(new_row):
                    result.content[y][x] = rock

        case Direction.north | Direction.south:
            for x, column in enumerate(grid.columns):
                new_column = slide_rocks(tuple(column), backwards=(direction == Direction.north))

                for y, rock in enumerate(new_column):
                    result.content[y][x] = rock

    return result

@cache
def do_cycle(grid: Grid):
    dirs = [
        Direction.north,
        Direction.west,
        Direction.south,
        Direction.east,
    ]

    for direction in dirs:
        grid = tilt(grid, direction)

    return grid

def calculate_load(grid: Grid):
    load = 0
    for n, row in enumerate(grid.rows):
        for rock in row:
            if rock == 'O':
                load += grid.height - n
    
    return load

def solve_part1(data: list[str]) -> int:
    grid = extract_info(data)

    grid = tilt(grid, Direction.north)

    return calculate_load(grid)


def solve_part2(data: list[str]) -> int:
    grid = extract_info(data)

    cycles = 1000

    for n in range(cycles):
        grid = do_cycle(grid)
        print(f"Cycle {100 * n/cycles:4.2f}% ({n}/{cycles}) {calculate_load(grid)}")


    return calculate_load(grid)


def main() -> None:
    with open("input/day14.txt", 'r') as data_file:
        data: list[str] = data_file.read().splitlines()

    print("Part 1:", solve_part1(data))
    print("Part 2:", solve_part2(data))


if __name__ == '__main__':
    main()