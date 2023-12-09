import unittest

import aoc.day09 as day09

_INPUT = """0 3 6 9 12 15
1 3 6 10 15 21
10 13 16 21 30 45"""

class TestDay09(unittest.TestCase):
    def test_part_1(self):
        self.assertEqual(day09.solve_part1(_INPUT.splitlines()), 114)

    def test_part_2(self):
        self.assertEqual(day09.solve_part2(_INPUT.splitlines()), 2)

if __name__ == '__main__':
    unittest.main()