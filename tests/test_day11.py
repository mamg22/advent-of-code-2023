import unittest

import aoc.day11 as day11

_INPUT = """...#......
.......#..
#.........
..........
......#...
.#........
.........#
..........
.......#..
#...#....."""

class TestDay11(unittest.TestCase):
    def test_part_1(self):
        self.assertEqual(day11.solve_part1(_INPUT.splitlines()), 374)

    def test_part_2a(self):
        self.assertEqual(day11.solve_part2(_INPUT.splitlines(), 10), 1030)

    def test_part_2b(self):
        self.assertEqual(day11.solve_part2(_INPUT.splitlines(), 100), 8410)

if __name__ == '__main__':
    unittest.main()