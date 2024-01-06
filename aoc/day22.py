from collections import Counter, deque
from collections.abc import Sequence
from dataclasses import dataclass
from itertools import product, groupby, count
from operator import attrgetter
from typing import Any, Generator, Iterator, Self


@dataclass(slots=True, order=True)
class Vector3d:
    x: int
    y: int
    z: int

    def __add__(self, other: Self) -> Self:
        return self.__class__(self.x + other.x, self.y + other.y, self.z + other.z)
    
    def __sub__(self, other: Self) -> Self:
        return self.__class__(self.x - other.x, self.y - other.y, self.z + other.z)
    
    def __neg__(self) -> Self:
        return self.__class__(-self.x, -self.y, -self.z)

    def __mul__(self, scalar: int):
        return self.__class__(self.x * scalar, self.y * scalar, self.z * scalar)

    def __repr__(self):
        return f"{self.__class__.__name__}({self.x}, {self.y}, {self.z})"
    
    def __hash__(self):
        return hash((self.x, self.y, self.z))

    def __iter__(self) -> Iterator[int]:
        return iter((self.x, self.y, self.z))

    def unpack(self) -> tuple[int, int, int]:
        return (self.x, self.y, self.z)


class Brick:
    start: Vector3d
    end: Vector3d
    children: set[Self]
    parents: set[Self]
    removable: bool
    _id = count()

    def __init__(self: Self, start: Vector3d, end: Vector3d) -> None:
        self.start = start
        self.end = end
        self.children = set()
        self.parents = set()
        self.removable = False
        self.id = next(self._id)

    
    @property
    def size(self: Self) -> Vector3d:
        return self.end - self.start + Vector3d(1, 1, 1)
    

    def add_child(self: Self, brick: Self) -> None:
        self.children.add(brick)
        brick.parents.add(self)

    
    class _BrickIterator:
        def __init__(self: Self, brick: 'Brick') -> None:
            self.generator = product(
                range(brick.start.x, brick.end.x + 1),
                range(brick.start.y, brick.end.y + 1),
                range(brick.start.z, brick.end.z + 1),
            )

        def __iter__(self: Self) -> Self:
            return self
        
        def __next__(self: Self) -> Vector3d:
            return Vector3d(*next(self.generator))


    def __iter__(self: Self):        
        return self._BrickIterator(self)


    def __hash__(self):
        return hash((self.start, self.end))
    

    def __repr__(self: Self) -> str:
        return f"{self.__class__.__name__}(start={self.start}, end={self.end})"


def parse_line(line: str) -> Brick:
    start_data, end_data = line.split('~')
    start = Vector3d(*(int(n) for n in start_data.split(",")))
    end = Vector3d(*(int(n) for n in end_data.split(",")))

    return Brick(start, end)


def parse_input(data: Sequence[str]) -> list[Brick]:
    bricks = sorted([parse_line(line) for line in data], key=attrgetter('start.z'))

    root_width, root_height = required_space(bricks)
    root_brick = Brick(Vector3d(0, 0, 0), Vector3d(root_width, root_height, 0))

    bricks.insert(0, root_brick)

    return bricks


def required_space(bricks: Sequence[Brick]) -> tuple[int, int]:
    max_x = 0
    max_y = 0
    for brick in bricks:
        max_x = max(max_x, brick.end.x)
        max_y = max(max_y, brick.end.y)
    
    return (max_x, max_y)


def fall_distance(brick: Brick, height: int) -> int:
    return max(brick.start.z - height - 1, 0)


def process_fall(bricks: list[Brick]) -> None:
    width = bricks[0].end.x + 1
    depth = bricks[0].end.y + 1

    height_matrix = [[0] * width for _ in range(depth)]

    for brick in bricks:
        distance = bricks[-1].end.z

        for x, y, z in brick:
            distance = min(distance, fall_distance(brick, height_matrix[y][x]))

        brick.start.z -= distance
        brick.end.z -= distance
        
        for x, y, z in brick:
            height_matrix[y][x] = max(z, height_matrix[y][x])
    
    bricks.sort(key=attrgetter('start.z'))


def build_tree(bricks: list[Brick]):
    groups: dict[int, list[Brick]] = {}

    for height, brick_group in groupby(bricks[1:], key=lambda brick: brick.start.z):
        groups[height] = list(brick_group)

    floor = bricks[0]

    to_check: deque[Brick] = deque([floor])
    checked: set[Brick] = set()

    while to_check:
        brick = to_check.popleft()
        if brick in checked:
            continue
        checked.add(brick)

        for x, y, z in brick:
            try:
                upper_pos = Vector3d(x, y, z + 1)
                for upper_brick in groups[z + 1]:
                    if upper_pos in upper_brick:
                        brick.add_child(upper_brick)
                        to_check.append(upper_brick)
            except KeyError:
                continue


def mark_removable(bricks: Sequence[Brick]):
    for brick in bricks:
        if not brick.children:
            brick.removable = True
            continue

        dependant_childs = [len(c.parents) > 1 for c in brick.children]
        brick.removable = all(dependant_childs)
        
        

def solve_part1(data: Sequence[str]) -> int:
    bricks = parse_input(data)

    process_fall(bricks)
    
    build_tree(bricks)

    mark_removable(bricks)
    total_dead = sum(1 for brick in bricks if brick.removable)

    return total_dead


def calculate_falls(node):
    to_check: deque[Brick] = deque([node])
    passed: set[Brick] = set()

    while to_check:
        current_node = to_check.popleft()

        if current_node.parents.issubset(passed) or current_node == node:
            if current_node not in passed:
                passed.add(current_node)
                to_check.extend(current_node.children)
    
    # Substract the start node, which is disintegrated and doesn't fall
    return len(passed) - 1


def solve_part2(data: Sequence[str]) -> int:
    bricks = parse_input(data)

    process_fall(bricks)
    
    build_tree(bricks)

    mark_removable(bricks)

    total = 0
    for brick in bricks[1:]:
        if brick.removable:
            continue

        falls = calculate_falls(brick)

        total += falls
    
    return total


def main() -> None:
    with open("input/day22.txt", 'r') as data_file:
        data: list[str] = data_file.read().splitlines()

    print("Part 1:", solve_part1(data))
    print("Part 2:", solve_part2(data))


if __name__ == '__main__':
    main()
