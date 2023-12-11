from dataclasses import dataclass
from itertools import combinations
import math

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



def extract_info(data: list[str], empty_cost: int):
    width = len(data[0])
    height = len(data)

    galaxies = []
    h_costs = [empty_cost for _ in range(width)]
    v_costs = [empty_cost for _ in range(height)]

    for y, line in enumerate(data):
        for x, cell in enumerate(line):
            if cell == '#':
                galaxies.append(Vector2d(x, y))
    
    for galaxy in galaxies:
        h_costs[galaxy.x] = 1
        v_costs[galaxy.y] = 1
    
    return galaxies, h_costs, v_costs


def get_total_distances(galaxies: list[Vector2d], h_costs: list[int], v_costs: list[int]):
    total_distance = 0
    for a, b in combinations(galaxies, 2):
        distance = 0

        for h in range(a.x, b.x, int(math.copysign(1, b.x - a.x))):
            distance += h_costs[h]

        for v in range(a.y, b.y, int(math.copysign(1, b.y - a.y))):
            distance += v_costs[v]
                
        total_distance += distance
    
    return total_distance


def solve_part1(data: list[str]) -> int:
    galaxies, h_costs, v_costs = extract_info(data, 2)
    return get_total_distances(galaxies, h_costs, v_costs)


def solve_part2(data: list[str], expansion_factor: int) -> int:
    galaxies, h_costs, v_costs = extract_info(data, expansion_factor)
    return get_total_distances(galaxies, h_costs, v_costs)


def main() -> None:
    with open("input/day11.txt", 'r') as data_file:
        data: list[str] = data_file.read().splitlines()

    print("Part 1:", solve_part1(data))
    print("Part 2:", solve_part2(data, 1_000_000))


if __name__ == '__main__':
    main()