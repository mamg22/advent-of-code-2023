import unittest

import aoc.day18 as day18

_INPUT = R'''
R 6 (#70c710)
D 5 (#0dc571)
L 2 (#5713f0)
D 2 (#d2c081)
R 2 (#59c680)
D 2 (#411b91)
L 5 (#8ceee2)
U 2 (#caa173)
L 1 (#1b58a2)
U 2 (#caa171)
R 2 (#7807d2)
U 3 (#a77fa3)
L 2 (#015232)
U 2 (#7a21e3)
'''.strip().splitlines()

# _INPUT = R'''
# R 2 (#000000)
# D 2 (#000000)
# L 2 (#000000)
# U 2 (#000000)
# '''.strip().splitlines()


class TestDay18(unittest.TestCase):
    def test_part_1(self):
        self.assertEqual(day18.solve_part1(_INPUT), 62)

    def test_part_2(self):
        self.assertEqual(day18.solve_part2(_INPUT), 952408144115)

if __name__ == '__main__':
    unittest.main()