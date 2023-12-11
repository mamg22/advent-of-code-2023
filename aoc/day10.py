from dataclasses import dataclass
from enum import Enum, auto

class Grid:
    def __init__(self, width: int, height:int, default_value=None):
        self.width = width
        self.height = height
        self.content = [[default_value] * width for _ in range(height)]
    
    def get(self, x: int, y: int):
        if x < 0 or x > self.width or y < 0 or y > self.height:
            raise IndexError(f"({x}, {y}) is out of grid area")
        return self.content[y][x]

    def set(self, x: int, y: int, value):
        if x < 0 or x > self.width or y < 0 or y > self.height:
            raise IndexError(f"({x}, {y}) is out of grid area")
        self.content[y][x] = value

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


class Cell:
    class Type(Enum):
        vertical = '|'
        horizontal = '-'
        up_right = 'L'
        up_left = 'J'
        down_left = '7'
        down_right = 'F'
        empty = '.'
        start = 'S'


    def __init__(self, celltype: 'Cell.Type', position: Vector2d):
        self.type = celltype
        self.position = position
    

    def __repr__(self):
        return f"Cell({self.type}, {self.position})"

    @property
    def openings(self):
        match self.type:
            case Cell.Type.vertical:
                return [Direction.north, Direction.south]
            case Cell.Type.horizontal:
                return [Direction.east, Direction.west]
            case Cell.Type.up_right:
                return [Direction.north, Direction.east]
            case Cell.Type.up_left:
                return [Direction.north, Direction.west]
            case Cell.Type.down_left:
                return [Direction.south, Direction.west]
            case Cell.Type.down_right:
                return [Direction.south, Direction.east]
            case Cell.Type.start:
                return [Direction.east, Direction.south, Direction.west, Direction.north]
            case _:
                return []


    def get_next_direction(self, current_direction: Direction):
        if self.type == Cell.Type.start:
            return current_direction
        
        complement = current_direction.complement

        return next(filter(lambda dir: dir != complement, self.openings), None)


def extract_info(data: list[str]) -> Grid:
    world = Grid(len(data[0]), len(data))

    for y, line in enumerate(data):
        for x, char in enumerate(line):
            cell = Cell(Cell.Type(char), Vector2d(x, y))
            world.set(x, y, cell)

            if (cell.type == Cell.Type.start):
                start_pos = Vector2d(x, y)

    return world, start_pos


def get_loop(world: Grid, start_pos: Vector2d):
    for direction in Direction:
        chain = []
        position = start_pos
        left_start = False

        while position != start_pos or not left_start:
            left_start = True

            current_cell = world.get(position.x, position.y)
            
            try:
                next_pos = position + direction.as_vector()
                next_cell = world.get(next_pos.x, next_pos.y)
            except IndexError:
                break

            if direction.complement in next_cell.openings:
                chain.append(current_cell)
                position = position + direction.as_vector()
                direction = next_cell.get_next_direction(direction)
            else:
                break
        else:
            break
    
    start_cell = chain[0]
    first_cell = chain[1]
    last_cell  = chain[-1]

    # Replace the start with its missing piece
    for pipe_type in Cell.Type:
        dirs = []
        start_cell.type = pipe_type

        complemented_openings = [op.complement for op in start_cell.openings]

        for direction in first_cell.openings:
            if first_cell.position + direction.as_vector() == start_cell.position:
                dirs.append(direction)

        for direction in last_cell.openings:
            if last_cell.position + direction.as_vector() == start_cell.position:
                dirs.append(direction)
        
        if len(set(complemented_openings) & set(dirs)) == 2:
            break
    
    return chain

def solve_part1(data: list[str]) -> int:
    world, start_pos = extract_info(data)
    loop = get_loop(world, start_pos)

    return len(loop) // 2


def solve_part2(data: list[str]) -> int:
    world, start_pos = extract_info(data)
    loop = get_loop(world, start_pos)

    ENTRY_POINTS = {
        Cell.Type.vertical,
        Cell.Type.up_left,
        Cell.Type.down_left,
        Cell.Type.up_right,
        Cell.Type.down_right,

    }


    EXIT_POINTS = {
        Cell.Type.vertical,
        Cell.Type.up_right,
        Cell.Type.down_right,
        Cell.Type.up_left,
        Cell.Type.down_left,
    }


    inner_spaces = 0
    for row in world.content:
        inside = False
        for cell in row:
            if cell in loop:
                if Direction.north in cell.openings:
                    inside = not inside
            elif inside and cell not in loop:
                inner_spaces += 1

    return inner_spaces

def main() -> None:
    with open("input/day10.txt", 'r') as data_file:
        data: list[str] = data_file.read().splitlines()

    print("Part 1:", solve_part1(data))
    print("Part 2:", solve_part2(data))


if __name__ == '__main__':
    main()