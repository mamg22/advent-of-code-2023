from collections import defaultdict
from functools import reduce

LIMITS = {
    'red': 12,
    'green': 13,
    'blue': 14,
}

def process_game_set(game, set_str: str):
    colors = {}

def process_game(game_str: str):
    colors = {}
    game_sets = game_str.split("; ")

    for game_set in game_sets:
        set_colors = defaultdict(int)
        cube_groups = game_set.split(", ")

        for cube_group in cube_groups:
            count, color = cube_group.strip().split(" ")
            count = int(count)
            set_colors[color] += count

        for color in set_colors:
            colors[color] = max(set_colors[color], colors.get(color, 0))

    return colors

def is_valid_game(game_colors):
    return all([
        game_colors[color] <= LIMITS[color]
        for color
        in game_colors
    ])

def solve_part1(data: list[str]):
    total = 0
    for line in data:
        game_info, game_results = line.split(": ", 1)

        game_id = int(game_info.split(" ")[1])
        game_colors = process_game(game_results)

        if is_valid_game(game_colors):
            total += game_id
    
    return total

def solve_part2(data: list[str]):
    total = 0
    for line in data:
        game_results = line.split(": ", 1)[1]

        game_colors = process_game(game_results)

        total += reduce(lambda a, b: a * b, game_colors.values())
    
    return total

def main():
    with open("input/day02.txt", 'r') as data_file:
        data: list[str] = data_file.readlines()

    print("Part 1:", solve_part1(data))
    print("Part 2:", solve_part2(data))

if __name__ == '__main__':
    main()