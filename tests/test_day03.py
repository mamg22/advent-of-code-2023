import unittest

import aoc.day03 as day03

_INPUT = """467..114..
...*......
..35..633.
......#...
617*......
.....+.58.
..592.....
......755.
...$.*....
.664.598..
"""

class TestDay03(unittest.TestCase):
    def test_part_1(self):
        self.assertEqual(day03.solve_part1(_INPUT.splitlines()), 4361)

    def test_part_2(self):
        self.assertEqual(day03.solve_part2(_INPUT.splitlines()), 467835)

if __name__ == '__main__':
    unittest.main()