import unittest

import aoc.day13 as day13

_INPUT = """
#.##..##.
..#.##.#.
##......#
##......#
..#.##.#.
..##..##.
#.#.##.#.

#...##..#
#....#..#
..##..###
#####.##.
#####.##.
..##..###
#....#..#
""".strip()

class TestDay13(unittest.TestCase):
    def test_part_1(self):
        self.assertEqual(day13.solve_part1(_INPUT.splitlines()), 405)

    def test_part_2(self):
        self.assertEqual(day13.solve_part2(_INPUT.splitlines()), 400)

if __name__ == '__main__':
    unittest.main()