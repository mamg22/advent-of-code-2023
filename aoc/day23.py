from collections.abc import Sequence
from dataclasses import dataclass, field
from enum import Enum, auto
from itertools import product
from typing import Optional, Self        


@dataclass(slots=True, order=True, frozen=True)
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


_infinity = float("+Infinity")


@dataclass(slots=True)
class Node:
    position: Vector2d
    content: str
    distance: int | float = _infinity
    previous: Optional[Self] = None
    edges: list['Edge'] = field(default_factory=list)
    visited: bool = False


    def add_edge(self: Self, edge: 'Edge') -> None:
        if edge not in self.edges:
            self.edges.append(edge)

    def __repr__(self):
        name = self.__class__.__name__
        return f"{name}({self.position})"
    
    def __hash__(self):
        return id(self)


@dataclass(slots=True)
class Edge:
    cost: int
    target: Node


def build_paths(data: Sequence[str], slopes: bool) -> tuple[dict[Vector2d, Node], Vector2d, Vector2d]:
    width, height = len(data[0]), len(data)
    start = Vector2d(data[0].index('.'), 0)
    end = Vector2d(data[-1].index('.'), height - 1)


    SLOPE_DIRECTIONS = {
        '>': Direction.east,
        'v': Direction.south,
        '<': Direction.west,
        '^': Direction.north,
    }


    nodes: dict[Vector2d, Node] = {
        pos: Node(pos, data[pos.y][pos.x])
        for pos in (
            Vector2d(x, y) for y, x in product(range(height), range(width))
            if data[y][x] != '#'
            )
        }
    
    for position, node in nodes.items():
        for direction in Direction:
            target_position = position + direction.as_vector()
            
            target = nodes.get(target_position)

            if not target:
                continue

            if slopes and direction.complement == SLOPE_DIRECTIONS.get(target.content):
                continue

            node.add_edge(Edge(1, target))
    
    simplify(nodes)
    
    return nodes, start, end


def get_reciprocal_edge(source: Node, target: Node) -> Optional[Edge]:
    return next(filter(lambda e: e.target is source, target.edges), None)


def detach_node(node: Node) -> None:
    target_a, target_b = node.edges
    reciprocal_a, reciprocal_b = (get_reciprocal_edge(node, edge.target) for edge in node.edges)

    if reciprocal_a is None or reciprocal_b is None:
        return

    reciprocal_a.target = target_b.target
    reciprocal_a.cost += target_b.cost

    reciprocal_b.target = target_a.target
    reciprocal_b.cost += target_a.cost

    node.edges.clear()


def simplify(nodes: dict[Vector2d, Node]) -> None:
    """
    Simplify graph by removing non-terminal and non-branching nodes,
    and updating the neighboring nodes' edges
    """

    to_remove: list[Vector2d] = []

    for node in nodes.values():
        if len(node.edges) != 2:
            continue

        if all(edge.target.content in '>v<^' for edge in node.edges):
            continue

        detach_node(node)
        to_remove.append(node.position)

    # Remove orphaned
    for position in to_remove:
        del nodes[position]


def dfs(root: Node, target: Node) -> int:
    root.visited = True

    length = max(
        (edge.cost + dfs(edge.target, target)
         for edge in root.edges
         if not edge.target.visited),
        default=0
        )
    
    root.visited = False

    NON_EXIT_PENALTY = -1000000
    if length == 0 and root is not target:
        length = NON_EXIT_PENALTY

    return length


def solve_part1(data: Sequence[str]) -> int:
    paths, start, end = build_paths(data, slopes=True)
    path_lengths = dfs(paths[start], paths[end])

    return path_lengths


def solve_part2(data: Sequence[str]) -> int:
    paths, start, end = build_paths(data, slopes=False)
    path_lengths = dfs(paths[start], paths[end])

    return path_lengths


def main() -> None:
    with open("input/day23.txt", 'r') as data_file:
        data: list[str] = data_file.read().splitlines()

    print("Part 1:", solve_part1(data))
    print("Part 2:", solve_part2(data))


if __name__ == '__main__':
    main()
