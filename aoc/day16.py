from enum import Enum, auto
from dataclasses import dataclass
from itertools import chain
from typing import Self, Any

@dataclass(slots=True)
class Vector2d:
    x: int
    y: int

    def __add__(self, other: Self) -> Self:
        return self.__class__(self.x + other.x, self.y + other.y)
    
    def __sub__(self, other: Self) -> Self:
        return self.__class__(self.x - other.x, self.y - other.y)
    
    def __neg__(self) -> Self:
        return self.__class__(-self.x, -self.y)
    
    def __hash__(self):
        return hash((self.x, self.y))

class Grid:
    def __init__(self, width: int, height: int, default_value: Any = None):
        self.width = width
        self.height = height
        self.content = [[default_value] * width for _ in range(height)]
    
    def get(self, x: int, y: int) -> Any:
        if x < 0 or y < 0:
            raise IndexError(f"({x}, {y}) is out of grid")
        return self.content[y][x]

    def set(self, x: int, y: int, value: Any) -> None:
        if x < 0 or y < 0:
            raise IndexError(f"({x}, {y}) is out of grid")
        self.content[y][x] = value


class Direction(Enum):
    east = auto()
    south = auto()
    west = auto()
    north = auto()

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
class Tile:
    class Type(Enum):
        empty = '.'
        right_mirror = '/'
        left_mirror = '\\'
        horizontal_splitter = '-'
        vertical_spliter = '|'

    def __init__(self, type_str: str) -> None:
        self.type = self.Type(type_str)
        self.energized = False
        self.visited = set()
    
    def transform_vector(self, vector: Vector2d) -> Vector2d:
        if self.type is self.Type.right_mirror:
            return Vector2d(-vector.y, -vector.x)
        elif self.type is self.Type.left_mirror:
            return Vector2d(vector.y, vector.x)
        else:
            return vector

    def reset(self) -> None:
        self.energized = False
        self.visited = set()

            

@dataclass
class Beam:
    position: Vector2d
    direction: Vector2d

def extract_grid(data: list[str]) -> Grid:
    grid = Grid(len(data[0]), len(data))

    for y, line in enumerate(data):
        for x, cell in enumerate(line):
            grid.set(x, y, Tile(cell))
    
    return grid

def trace_beam(grid: Grid, beam: Beam):
    beams = [beam]

    while len(beams) > 0:
        beam = beams[0]
        try:
            current_tile = grid.get(beam.position.x, beam.position.y)
            current_tile.energized = True
        except IndexError:
            # Beam went off-grid, no longer needed
            beams.remove(beam)
            continue

        if beam.direction in current_tile.visited:
            beams.remove(beam)
            continue
        else:
            current_tile.visited.add(beam.direction)

        match current_tile.type:
            case Tile.Type.horizontal_splitter if beam.direction.y != 0:
                beams.remove(beam)
                beams.extend([
                    Beam(beam.position + Vector2d(-1, 0), Direction.west.as_vector()),
                    Beam(beam.position + Vector2d(1, 0), Direction.east.as_vector()),
                ])
            case Tile.Type.vertical_spliter if beam.direction.x != 0:
                beams.remove(beam)
                beams.extend([
                    Beam(beam.position + Vector2d(0, -1), Direction.north.as_vector()),
                    Beam(beam.position + Vector2d(0, 1), Direction.south.as_vector()),
                ])
            case _:
                new_direction = current_tile.transform_vector(beam.direction)
                new_position = beam.position + new_direction

                beam.direction = new_direction
                beam.position = new_position
    
    total = 0
    for row in grid.content:
        for tile in row:
            total += 1 if tile.energized else 0
    
    return total


def solve_part1(data: list[str]) -> int:
    grid = extract_grid(data)
    beam = Beam(Vector2d(0, 0), Direction.east.as_vector())

    return trace_beam(grid, beam)

def solve_part2(data: list[str]) -> int:
    grid = extract_grid(data)

    beams = chain(
        (
            Beam(Vector2d(0, y), Direction.east.as_vector())
            for y in range(grid.height)
        ),
        (
            Beam(Vector2d(x, 0), Direction.south.as_vector())
            for x in range(grid.width)
        ),
        (
            Beam(Vector2d(grid.width - 1, y), Direction.west.as_vector())
            for y in range(grid.height)
        ),
        (
            Beam(Vector2d(x, grid.height - 1), Direction.north.as_vector())
            for x in range(grid.width)
        ),
    )

    best = 0

    for n, beam in enumerate(beams):
        beam_energized = trace_beam(grid, beam)
        best = max(best, beam_energized)
        # print(f"Beam {n}/{grid.width * 2 + grid.height * 2}: Energized = {beam_energized}, Best = {best}")

        # Reset the grid
        for row in grid.content:
            for tile in row:
                tile.reset()


    return best


def main() -> None:
    with open("input/day16.txt", 'r') as data_file:
        data: list[str] = data_file.read().splitlines()

    print("Part 1:", solve_part1(data))
    print("Part 2:", solve_part2(data))


if __name__ == '__main__':
    main()