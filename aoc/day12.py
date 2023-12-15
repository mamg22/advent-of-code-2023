from enum import StrEnum
from functools import cache, reduce


class Spring(StrEnum):
    operative = '.'
    damaged = '#'
    unknown = '?'

    def __repr__(self):
        return f"{self.value}"


Spring_list = list[tuple[tuple[Spring], tuple[int]]]


def extract_info(data: list[str], folded: bool) -> Spring_list:
    springs: Spring_list = []

    if folded:
        multiplier = 5
    else:
        multiplier = 1

    for line in data:
        field_str, clue_str = line.split()

        # Multiply the string [multiplier] times with a ? in between
        field_str = '?'.join([field_str] * multiplier)

        springs.append(
            (
                tuple(Spring(ch) for ch in field_str),
                tuple(int(n) for n in clue_str.split(',')) * multiplier,
            )
        )
    
    return springs


@cache
def simple_solve(springs: tuple[Spring], clues: tuple[int]):
    if not clues:
        if Spring.damaged in springs:
            return 0
        else:
            return 1
    
    match springs:
        case (Spring.operative, *_):
            return simple_solve(springs[1:], clues)
        
        case (Spring.damaged, *_):
            try:
                can_place = all(springs[i] != Spring.operative for i in range(clues[0]))
            except IndexError:
                can_place = False
            
            if can_place and (len(springs) == clues[0] or springs[clues[0]] != Spring.damaged):
                return simple_solve(springs[clues[0] + 1:], clues[1:])
            else:
                return 0


        case (Spring.unknown, *_):
            branch_operative = (Spring.operative,) + springs[1:]
            branch_damaged = (Spring.damaged,) + springs[1:]

            return simple_solve(branch_operative, clues) + simple_solve(branch_damaged, clues)
        
        case _:
            return 0



def solve_part1(data: list[str]) -> int:
    spring_lines = extract_info(data, folded=False)

    return sum(map(lambda line: simple_solve(*line), spring_lines))


def solve_part2(data: list[str]) -> int:
    spring_lines = extract_info(data, folded=True)

    return sum(map(lambda line: simple_solve(*line), spring_lines))


def main() -> None:
    with open("input/day12.txt", 'r') as data_file:
        data: list[str] = data_file.read().splitlines()

    print("Part 1:", solve_part1(data))
    print("Part 2:", solve_part2(data))


if __name__ == '__main__':
    main()