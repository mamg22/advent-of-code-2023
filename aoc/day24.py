from collections.abc import Sequence
from copy import deepcopy
from dataclasses import dataclass
from itertools import combinations
from math import copysign
from typing import Iterator, Self

@dataclass(slots=True, order=True, frozen=True)
class Vector3d:
    x: float
    y: float
    z: float

    def __add__(self, other: Self) -> Self:
        return self.__class__(self.x + other.x, self.y + other.y, self.z + other.z)
    
    def __sub__(self, other: Self) -> Self:
        return self.__class__(self.x - other.x, self.y - other.y, self.z + other.z)
    
    def __neg__(self) -> Self:
        return self.__class__(-self.x, -self.y, -self.z)

    def __mul__(self, scalar: float):
        return self.__class__(self.x * scalar, self.y * scalar, self.z * scalar)

    def __repr__(self):
        return f"{self.__class__.__name__}({self.x}, {self.y}, {self.z})"
    
    def __hash__(self):
        return hash((self.x, self.y, self.z))
    

@dataclass(frozen=True)
class Hailstone:
    position: Vector3d
    velocity: Vector3d


def parse_vector(vector_str: str) -> Vector3d:
    return Vector3d(*(map(lambda num: int(num.strip()), vector_str.strip().split(','))))


def parse_line(line: str) -> Hailstone:
    pos_str, vel_str = line.split('@')

    return Hailstone(parse_vector(pos_str), parse_vector(vel_str))



def parse_input(data: Sequence[str]) -> list[Hailstone]:
    return [parse_line(line) for line in data]


# Based on https://en.wikipedia.org/wiki/Line%E2%80%93line_intersection#Given_two_points_on_each_line_segment
def intersect2d(a: Hailstone, b: Hailstone):
    a0 = a.position
    a1 = a.position + a.velocity
    b0 = b.position
    b1 = b.position + b.velocity

    x1, y1 = a0.x, a0.y
    x2, y2 = a1.x, a1.y
    x3, y3 = b0.x, b0.y
    x4, y4 = b1.x, b1.y

    t_numerator   = (x1 - x3) * (y3 - y4) - (y1 - y3) * (x3 - x4)
    t_denominator = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)

    u_numerator   = (x1 - x2) * (y1 - y3) - (y1 - y2) * (x1 - x3)
    u_denominator = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)

    try:
        t = t_numerator / t_denominator
        u = u_numerator / u_denominator
    except ZeroDivisionError:
        return None

    intersection = Vector3d(x1 + t * (x2 - x1), y1 + t * (y2 - y1), 0)

    # Require that the difference between intersection and position, and the velocity
    # have the same x direction. If true, the stones are heading towards each other,
    # otherwise, they are moving further apart.
    a_delta_dir = copysign(1, intersection.x - a.position.x)
    a_dir = copysign(1, a.velocity.x)
    b_delta_dir = copysign(1, intersection.x - b.position.x)
    b_dir = copysign(1, b.velocity.x)

    if a_delta_dir != a_dir or b_delta_dir != b_dir:
        return None 

    return intersection
    

def check_bounds(intersection: Vector3d, bounds: tuple[float, float]):
    return (
        bounds[0] <= intersection.x <= bounds[1] and
        bounds[0] <= intersection.y <= bounds[1]
    )


def solve_part1(data: Sequence[str], bounds: tuple[float, float]) -> int:
    hailstones = parse_input(data)

    total = 0

    for a, b in combinations(hailstones, 2):
        intersection = intersect2d(a, b)

        if intersection is not None and check_bounds(intersection, bounds):
            total += 1

    return total


# Many parts of this code ported to Python from:
# https://github.com/tckmn/polyaoc-2023/blob/97689dc6b5ff38c557cd885b10be425e14928958/24/rb/24.rb#L22
# among other hints and tips from other shared solutions

def gaussian_elimination(matrix: list[list[float]]):
    m = deepcopy(matrix)

    for i in range(len(m)):
        t = m[i][i]

        if t == 0:
            # find a row below that has a nonzero element on the main diagonal
            for k in range(i + 1, len(m)):
                if m[k][i] != 0:
                    m[i], m[k] = m[k], m[i]
                    t = m[i][i]
                    break
            else:
                raise ValueError("No unique solution")

        m[i] = [x / t for x in m[i]]
        for j in range(i + 1, len(m)):
            t = m[j][i]
            m[j] = [x - t * m[i][k] for k, x in enumerate(m[j])]

    for i in range(len(m) - 1, -1, -1):
        for j in range(i):
            t = m[j][i]
            m[j] = [x - t * m[i][k] for k, x in enumerate(m[j])]

    return m

def generate_matrices(hailstones: list[Hailstone], properties: tuple[str, str]):
    m = [
        [
        -getattr(s.velocity, properties[1]),
        getattr(s.velocity, properties[0]),
        getattr(s.position, properties[1]),
        -getattr(s.position, properties[0]),
        (
            getattr(s.position, properties[1]) * getattr(s.velocity, properties[0]) -
            getattr(s.position, properties[0]) * getattr(s.velocity, properties[1])
        )] for s in hailstones]
        
    return [[a - b for a, b in zip(r, m[-1])] for r in m[:4]]

def solve_part2(data: Sequence[str]) -> int:
    hailstones = parse_input(data)
    xy_elim = gaussian_elimination(generate_matrices(hailstones, ('x', 'y')))
    zy_elim = gaussian_elimination(generate_matrices(hailstones, ('z', 'y')))
    
    x, y, *_ = [r[-1] for r in xy_elim]
    z, *_ = [r[-1] for r in zy_elim]
    
    return int(round(x) + round(y) + round(z))

def main() -> None:
    with open("input/day24.txt", 'r') as data_file:
        data: list[str] = data_file.read().splitlines()

    bounds=(200_000_000_000_000, 400_000_000_000_000)

    print("Part 1:", solve_part1(data, bounds=bounds))
    print("Part 2:", solve_part2(data))


if __name__ == '__main__':
    main()
