import unittest

import aoc.day24 as day24

_INPUT = R'''
19, 13, 30 @ -2,  1, -2
18, 19, 22 @ -1, -1, -2
20, 25, 34 @ -2, -2, -4
12, 31, 28 @ -1, -2, -1
20, 19, 15 @  1, -5, -3
'''.strip().splitlines()


class TestDay24(unittest.TestCase):
    def test_part_1(self):
        self.assertEqual(day24.solve_part1(_INPUT, (7, 27)), 2)

    def test_part_2(self):
        self.assertEqual(day24.solve_part2(_INPUT), 47)

if __name__ == '__main__':
    unittest.main()