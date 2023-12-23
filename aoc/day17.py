from enum import Enum, auto
from dataclasses import dataclass, field
from functools import total_ordering
import heapq
from typing import Self, Any, Optional, NamedTuple


_infinity = float("infinity")

PriorityQueue = list

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


def extract_grid(data: list[str]) -> Grid:
    grid = Grid(len(data[0]), len(data))

    for y, line in enumerate(data):
        for x, cell in enumerate(line):
            # Two sets of nodes, separated as planes
            # the first one is the horizontal plane
            # the second is the vertical plane
            # nodes in the horizontal plane connect to their neighbors
            # in the vertical plane, and viceversa
            cost = int(cell)

            if x == 0 and y == 0:
                cost = 0

            grid.set(x, y, Cell(
                Node(Vector2d(x, y), cost, Plane.horizontal),
                Node(Vector2d(x, y), cost, Plane.vertical),
            ))
    
    return grid


class Plane(Enum):
    vertical = auto()
    horizontal = auto()
    both = auto()

    def __repr__(self):
        return self.name[0].upper()


@total_ordering
@dataclass
class Node:
    position: Vector2d
    cost: int
    plane: Plane
    distance: int | float = _infinity
    previous: Optional[Self] = None
    visited: bool = False
    edges: list['Edge'] = field(default_factory=list)

    def __repr__(self):
        name = self.__class__.__name__
        plane = repr(self.plane)
        return f"{name}(pos=({self.position}), plane={plane}, cost={self.cost}, distance={self.distance})"
    
    def __gt__(self, other: Self):
        return self.distance > other.distance

    def __lt__(self, other: Self):
        return self.distance < other.distance

    def __hash__(self):
        return hash((self.cost, self.position, self.plane))


@dataclass
class Edge:
    cost: int | float
    target: Node


Cell = NamedTuple("Cell",[
    ('h', Node),
    ('v', Node)
])



def make_graph(grid: Grid, min_dist: int, max_dist: int) -> tuple[list[Node], Node, Node]:
    R"""
    Builds the graph based on the grid contents.

    Returns the graph, and the start and end nodes

    Due to the problem restricting straight line movement. This uses two
    planes of the grid: One being the horizontally moving plane, composed
    of all nodes whose movement goes east and west, and its complementary
    vertically moving plane with nodes going north and south.

    The resulting graph connects nodes in such a way that each movement jumps
    from one plane to the other. So if currently at (1, 1), coming from the
    north, the (1, 1) node we're on is the one from the horizontal plane,
    and then its edges at (0, 1), (1, 0) and so on, are all on the vertical plane.

    Two special nodes for the start and end are added, which exist in both planes
    and have no movement cost. The start node has the (0, 0) corner as its edges,
    connected to it in both planes. The end node does the same with the opposite corner.
    """

    nodes: list[Node] = []

    for y, row in enumerate(grid.content):
        for x, cell in enumerate(row):
            h_cell, v_cell = cell

            # Horizontal cell neighbors
            for direction in (Direction.east, Direction.west):
                cost = 0
                direction_multiplier = 1 if direction is Direction.east else -1
                for factor in range(1, max_dist):
                    try:
                        neighbor = grid.get(x + direction_multiplier * factor, y).v

                        cost += neighbor.cost
                    except IndexError:
                        break

                    if factor in range(min_dist, max_dist):
                        h_cell.edges.append(Edge(cost, neighbor))

            # Vertical cell neighbors
            for direction in (Direction.north, Direction.south):
                cost = 0
                direction_multiplier = 1 if direction is Direction.south else -1
                for factor in range(1, max_dist):
                    try:
                        neighbor = grid.get(x, y + direction_multiplier * factor).h

                        cost += neighbor.cost
                    except IndexError:
                        break

                    if factor in range(min_dist, max_dist):
                        v_cell.edges.append(Edge(cost, neighbor))

            nodes.append(cell.v)
            nodes.append(cell.h)
    

    start = Node(Vector2d(-1, -1), 0, Plane.both, distance=0)
    end = Node(Vector2d(grid.width, grid.height), 0, Plane.both)

    start.edges.extend([Edge(0, node) for node in grid.get(0, 0)])
    
    grid_end = grid.get(grid.width - 1, grid.height - 1)

    for plane_end in grid_end:
        plane_end.edges.append(Edge(0, end))

    nodes.append(start)
    nodes.append(end)

    return nodes, start, end


def dijkstra(start: Node, end: Node):
    queue: PriorityQueue = [start]

    while queue:
        node: Node = heapq.heappop(queue)

        if node.visited:
            continue
        else:
            node.visited = True

        for edge in node.edges:
            new_distance = node.distance + edge.cost

            if new_distance < edge.target.distance:
                edge.target.distance = new_distance
                edge.target.previous = node

            if not edge.target.visited:
                heapq.heappush(queue, edge.target)
    
    shortest_path: list[Node] = []
    current_node: Optional[Node] = end

    if current_node.previous or current_node is start:
        while current_node:
            shortest_path.append(current_node)
            current_node = current_node.previous

    shortest_path.reverse()

    return shortest_path

def solve_part1(data: list[str]) -> int:
    grid = extract_grid(data)
    graph, start, end = make_graph(grid, 1, 4)

    path = dijkstra(start, end)

    return int(path[-1].distance)

def solve_part2(data: list[str]) -> int:
    grid = extract_grid(data)
    graph, start, end = make_graph(grid, 4, 11)

    path = dijkstra(start, end)

    return int(path[-1].distance)


def main() -> None:
    with open("input/day17.txt", 'r') as data_file:
        data: list[str] = data_file.read().splitlines()

    print("Part 1:", solve_part1(data))
    print("Part 2:", solve_part2(data))


if __name__ == '__main__':
    main()