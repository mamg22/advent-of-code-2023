from itertools import count
from functools import partial
from typing import Iterator, Any, Optional


class Grid:
    def __init__(self, 
                 width: Optional[int] = None, height: Optional[int] = None,
                 default_value: Any = None, 
                 content: Optional[list[list[Any]]] = None):
        if content is not None:
            self._width = max(map(len, content))
            self._height = len(content)
            self.content = content.copy()
        else:
            if width is None or height is None:
                raise ValueError("Grid width or height cannot be None unless content is provided")
            
            self._width = width
            self._height = height
            self.content = [[default_value] * width for _ in range(height)]

    
    def get(self, x: int, y: int):
        if x < 0 or x > self.width or y < 0 or y > self.height:
            raise IndexError(f"({x}, {y}) is out of grid area")
        return self.content[y][x]

    def set(self, x: int, y: int, value: Any):
        if x < 0 or x > self.width or y < 0 or y > self.height:
            raise IndexError(f"({x}, {y}) is out of grid area")
        self.content[y][x] = value

    @property
    def width(self):
        return self._width
    
    @property
    def height(self):
        return self._height


def extract_info(data: list[str]) -> Iterator[Grid]:
    grid_content = []
    for line in data:
        if not line or line.isspace():
            yield Grid(content=grid_content)
            grid_content.clear()
            continue

        grid_content.append([ch == '#' for ch in line])
    else:
        yield Grid(content=grid_content)


def get_reflections(grid: Grid, with_smudge: bool) -> tuple[int, None] | tuple[None, int]:
    for offset in range(1, grid.height):
        smudge = False
        for y, inv_y in zip(count(offset), count(offset - 1, step=-1)):
            try:
                reflect = [
                    grid.get(x, y) == grid.get(x, inv_y)
                    for x in range(grid.width)
                ]

                if with_smudge and not smudge and reflect.count(False) == 1:
                    smudge = True
                    continue

                if not all(reflect):
                    break
            except IndexError:
                if not with_smudge or (with_smudge and smudge):
                    return (offset, None)
                else:
                    break

    for offset in range(1, grid.width):
        smudge = False
        for x, inv_x in zip(count(offset), count(offset - 1, step=-1)):
            try:
                reflect = [
                    grid.get(x, y) == grid.get(inv_x, y)
                    for y in range(grid.height)
                ]

                if with_smudge and not smudge and reflect.count(False) == 1:
                    smudge = True
                    continue


                if not all(reflect):
                    break
            except IndexError:
                if not with_smudge or (with_smudge and smudge):
                    return (None, offset)
                else:
                    break


def reflection_value(grid: Grid, with_smudge: bool):
    hr, vr = get_reflections(grid, with_smudge)

    hr = hr or 0
    vr = vr or 0

    return hr * 100 + vr


def solve_part1(data: list[str]) -> int:
    func = partial(reflection_value, with_smudge=False)
    return sum(map(func, extract_info(data)))

def solve_part2(data: list[str]) -> int:
    func = partial(reflection_value, with_smudge=True)
    return sum(map(func, extract_info(data)))


def main() -> None:
    with open("input/day13.txt", 'r') as data_file:
        data: list[str] = data_file.read().splitlines()

    print("Part 1:", solve_part1(data))
    print("Part 2:", solve_part2(data))


if __name__ == '__main__':
    main()