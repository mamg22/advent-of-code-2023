import unittest

import aoc.day21 as day21

_INPUT = R'''
...........
.....###.#.
.###.##..#.
..#.#...#..
....#.#....
.##..S####.
.##..#...#.
.......##..
.##.#.####.
.##..##.##.
...........
'''.strip().splitlines()


class TestDay21(unittest.TestCase):
    def test_part_1(self):
        self.assertEqual(day21.solve_part1(_INPUT, 6), 16)

    def test_part_2a(self):
        self.assertEqual(day21.solve_part1(_INPUT, 6), 16)

    def test_part_2b(self):
        self.assertEqual(day21.solve_part1(_INPUT, 10), 50)

    def test_part_2c(self):
        self.assertEqual(day21.solve_part1(_INPUT, 50), 1594)


if __name__ == '__main__':
    unittest.main()