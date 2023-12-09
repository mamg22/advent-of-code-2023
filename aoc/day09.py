from itertools import pairwise
from pprint import pprint

def extract_info(data: list[str]) -> list[list[int]]:
    return [
        [int(n) for n in line.split()]
        for line in data
    ]


def extrapolate(line: list[int]) -> int:
    sequences = [line]

    while not all(n == 0 for n in sequences[-1]):
        sequences.append([
            b - a for a, b in pairwise(sequences[-1])
        ])
    
    sequences[-1].append(0)

    for previous, current in pairwise(reversed(sequences)):
        current.append(previous[-1] + current[-1])
    
    return sequences


def solve_part1(data: list[str]) -> int:
    input_lines = extract_info(data)

    total = 0
    for line in input_lines:
        extrapolation = extrapolate(line)
        total += extrapolation[0][-1]

    return total

def solve_part2(data: list[str]) -> int:
    input_lines = extract_info(data)

    total = 0
    for line in input_lines:
        line.reverse()
        extrapolation = extrapolate(line)
        total += extrapolation[0][-1]

    return total


def main():
    with open("input/day09.txt", 'r') as data_file:
        data: list[str] = data_file.read().splitlines()

    print("Part 1:", solve_part1(data))
    print("Part 2:", solve_part2(data))


if __name__ == '__main__':
    main()