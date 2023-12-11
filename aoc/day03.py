import math
import string
from functools import reduce
from dataclasses import dataclass

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
@dataclass
class Element:
    def __init__(self, x, y):
        self.x = x
        self.y = y

@dataclass
class Number(Element):
    def __init__(self, x, y, initial_value=0):
        super().__init__(x, y)
        self.value = initial_value
        self.part = False
    
    def __repr__(self):
        return f"Number({self.value})"
    
    def insert(self, value):
        self.value = self.value * 10 + value

    def set_part(self, is_part):
        self.part = self.part or is_part

    @property
    def width(self):
        return len(str(self.value))

@dataclass
class Symbol(Element):
    def __init__(self, x, y, symbol):
        super().__init__(x, y)
        self.symbol = symbol
        self.neighbors = []

    def __repr__(self):
        return f"Symbol({self.symbol}, {self.neighbors})"

    def add_neighbor(self, neighbor):
        self.neighbors.append(neighbor)

def extract_info(data: list[str]):
    symbols: list[Symbol] = []
    numbers: list[Number] = []
    symbol_grid: Grid = Grid(len(data[0].strip()), len(data), False)
    current_number = None

    for y, line in enumerate(data):
        line = line.strip()

        for x, char in enumerate(line):
            if char.isdigit():
                if not current_number:
                    current_number = Number(x, y)

                char_value = int(char)
                current_number.insert(char_value)
            else:
                if char in string.punctuation and char != '.':
                    symbols.append(Symbol(x, y, char))
                    symbol_grid.set(x, y, True)

                if current_number:
                    numbers.append(current_number)
                current_number = None

        if current_number:
            numbers.append(current_number)
        current_number = None
    
    return (symbols, numbers, symbol_grid)


def solve_part1(data: list[str]):
    _, numbers, symbol_grid = extract_info(data)
    total = 0
    for number in numbers:
        for y in range(number.y - 1, number.y + 2):
            for x in range(number.x - 1, number.x + number.width + 1):
                try:
                    number.set_part(not not symbol_grid.get(x, y))
                except IndexError:
                    continue
        if number.part:
            total += number.value
    
    return total

def solve_part2(data: list[str]):
    symbols, numbers, _ = extract_info(data)

    gears = [elem for elem in symbols if elem.symbol == '*']
    gear_map = Grid(len(data[0].strip()), len(data))

    for gear in gears:
        gear_map.set(gear.x, gear.y, gear)

    for number in numbers:
        for y in range(number.y - 1, number.y + 2):
            for x in range(number.x - 1, number.x + number.width + 1):
                try:
                    if gear := gear_map.get(x, y):
                        gear.add_neighbor(number)
                except IndexError:
                    continue
    
    total = 0
    for gear in gears:
        if len(gear.neighbors) == 2:
            a, b = gear.neighbors
            total += a.value * b.value

    return total


def main():
    with open("input/day03.txt", 'r') as data_file:
        data: list[str] = data_file.readlines()
    
    print("Part 1:", solve_part1(data))
    print("Part 2:", solve_part2(data))

if __name__ == '__main__':
    main()