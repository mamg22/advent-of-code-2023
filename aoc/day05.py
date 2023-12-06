from dataclasses import dataclass

@dataclass
class Transform:
    def __init__(self, dest_pos, source_pos, length):
        self.dest_pos = dest_pos
        self.source_pos = source_pos
        self.length = length
        self.range = range(self.source_pos, self.source_pos + self.length)
    
    def __call__(self, value):
        delta = self.dest_pos - self.source_pos
        transformed = False
        if value in self.range:
            value += delta
            transformed = True
        return value, transformed

class Map:
    def __init__(self, source, destination):
        self.source = source
        self.destination = destination
        self.transforms = []
    
    def add_transform(self, dest_pos, source_pos, length):        
        self.transforms.append(Transform(dest_pos, source_pos, length))
    
    def apply_transforms(self, value):
        for transform in self.transforms:
            value, transformed = transform(value)
            if transformed:
                break
        return value

def extract_info(data: list[str]):
    seeds = [int(num) for num in data[0].split() if num.isdecimal()]

    map_lists = data[2:]

    current_map = None
    maps = []
    for line in map_lists:
        if line.endswith('map:'):
            transform_type = line.split()[0]
            source, _, destination = transform_type.split('-')
            current_map = Map(source, destination)
            maps.append(current_map)
        elif line and not line.isspace():
            destination, source, length = [int(n) for n in line.split()]
            current_map.add_transform(destination, source, length)

    return seeds, maps

def map_seed(seed: int, mappings: list[Map]):
    for mapping in mappings:
        seed = mapping.apply_transforms(seed)
    
    return seed

def solve_part1(data: list[str]) -> int:
    seeds, maps = extract_info(data)

    mapped_seeds = map(lambda seed: map_seed(seed, maps), seeds)
    
    return min(mapped_seeds)

def split_range(source: range, overlay: range) -> set[range]:
    splits = set()

    if overlay.start in source and overlay.stop in source:
        splits.add(range(source.start, overlay.start))
        splits.add(overlay)
        splits.add(range(overlay.stop, source.stop))
    elif overlay.start in source:
        splits.add(range(source.start, overlay.start))
        splits.add(range(overlay.start, source.stop))
    elif overlay.stop in source:
        splits.add(range(source.start, overlay.stop))
        splits.add(range(overlay.stop, source.stop))
    else:
        splits.add(source)
    
    return splits

def transform_range(value: range, mapping: Map):
    start, stop = value.start, value.stop

    start = mapping.apply_transforms(start)
    # Transform but move the stop point in-range temporarily
    # to properly transform it into its new range
    stop = mapping.apply_transforms(stop - 1) + 1

    return range(start, stop)

def solve_part2(data: list[str]) -> int:
    seeds, mappings = extract_info(data)

    seed_ranges: set[range] = set()
    for seeds_start, seeds_length in zip(seeds[::2], seeds[1::2]):
        seed_ranges.add(range(seeds_start, seeds_start + seeds_length))
    
    for mapping in mappings:
        new_seed_ranges = set()
        for seed_range in seed_ranges:
            new_seed_ranges.update(
                *[
                    split_range(seed_range, transform.range) for
                    transform in mapping.transforms
                ]
            )
            

        seed_ranges = {transform_range(r, mapping) for r in new_seed_ranges}

    mins = 99999999999999999999999999
    for r in seed_ranges:
        if r.start > 0:
            mins = min(mins, r.start)

    return mins

def main():
    with open("input/day05.txt", 'r') as data_file:
        data: list[str] = data_file.read().splitlines()

    print("Part 1:", solve_part1(data))
    print("Part 2:", solve_part2(data))

if __name__ == '__main__':
    main()