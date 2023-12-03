def extract_digit_numbers(line: str):
    return [int(ch) for ch in line if ch.isdigit()]

def replace_number_text(line: str):
    REPLACEMENTS = {
        'zero': '0ero',
        'one': '1ne',
        'two': '2wo',
        'three': '3hree',
        'four': '4our',
        'five': '5ive',
        'six': '6ix',
        'seven': '7even',
        'eight': '8ight',
        'nine': '9ine',
    }

    while True:
        indexes = {}
        for text in REPLACEMENTS:
            idx = line.find(text)
            if idx != -1:
                indexes[text] = idx

        if len(indexes) > 0:
            target = min(indexes.items(), key=lambda item: item[1])[0]
            line = line.replace(target, REPLACEMENTS[target], 1)
        else:
            break
    
    return line

def extract_all_numbers(line: str):
    return extract_digit_numbers(replace_number_text(line))

def solve_part1(data):
    total = 0
    for line in data:
        numbers = extract_digit_numbers(line)
        line_value = numbers[0] * 10 + numbers[-1]
        total += line_value
    
    return total

def solve_part2(data):
    total = 0
    for line in data:
        numbers = extract_all_numbers(line)
        line_value = numbers[0] * 10 + numbers[-1]
        total += line_value

    return total

if __name__ == '__main__':
    with open("input/day01.txt", 'r') as data_file:
        data: list[str] = data_file.readlines()

    p1 = solve_part1(data)
    p2 = solve_part2(data)
    
    print(f"Part 1: {p1}")
    print(f"Part 2: {p2}")
