import unittest

import aoc.day14 as day14

_INPUT = """
O....#....
O.OO#....#
.....##...
OO.#O....O
.O.....O#.
O.#..O.#.#
..O..#O..O
.......O..
#....###..
#OO..#....
""".strip()

class TestDay14(unittest.TestCase):
    def test_part_1(self):
        self.assertEqual(day14.solve_part1(_INPUT.splitlines()), 136)

    def test_part_2(self):
        self.assertEqual(day14.solve_part2(_INPUT.splitlines()), 64)

if __name__ == '__main__':
    unittest.main()