import unittest

import aoc.day06 as day06

_INPUT = """Time:      7  15   30
Distance:  9  40  200
"""

class TestDay06(unittest.TestCase):
    def test_part_1(self):
        self.assertEqual(day06.solve_part1(_INPUT.splitlines()), 288)

    def test_part_2(self):
        self.assertEqual(day06.solve_part2(_INPUT.splitlines()), 71503)

if __name__ == '__main__':
    unittest.main()