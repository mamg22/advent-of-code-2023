from functools import reduce

def extract_info(data: list[str], concatenate: bool = False) -> list[tuple[int, int]]:
    time_line = data[0].removeprefix("Time:").lstrip()
    distance_line = data[1].removeprefix("Distance:").lstrip()

    if concatenate:
        time_line = time_line.replace(' ', '')
        distance_line = distance_line.replace(' ', '')

    times = [int(n) for n in time_line.split()]
    distances = [int(n) for n in distance_line.split()]

    return list(zip(times, distances))

def solve_part1(data: list[str]) -> int:
    success_counts = []
    for time, distance in extract_info(data):
        successful = []
        for t in range(time + 1):
            travel = t * (time - t)
            if travel > distance:
                successful.append(t)
        success_counts.append(len(successful))

    return reduce(lambda a, b: a * b, success_counts)

def solve_part2(data: list[str]) -> int:
    time, distance = extract_info(data, True)[0]

    success_min = 0
    success_max = time

    for t in range(time + 1):
        travel = t * (time - t)
        if travel > distance:
            success_min = t
            break
    
    for t in range(time + 1, 0, -1):
        travel = t * (time - t)
        if travel > distance:
            # Add +1 to make is an inclusive range
            success_max = t + 1
            break

    return success_max - success_min

def main():
    with open("input/day06.txt", 'r') as data_file:
        data: list[str] = data_file.read().splitlines()

    print("Part 1:", solve_part1(data))
    print("Part 2:", solve_part2(data))

if __name__ == '__main__':
    main()