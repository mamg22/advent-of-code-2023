import unittest

import aoc.day10 as day10

_INPUT = """7-F7-
.FJ|7
SJLL7
|F--J
LJ.LJ
"""

_INPUT_2 = """..........
.S------7.
.|F----7|.
.||....||.
.||....||.
.|L-7F-J|.
.|..||..|.
.L--JL--J.
..........
"""

class TestDay10(unittest.TestCase):
    def test_part_1(self):
        self.assertEqual(day10.solve_part1(_INPUT.splitlines()), 8)

    def test_part_2(self):
        self.assertEqual(day10.solve_part2(_INPUT_2.splitlines()), 4)

if __name__ == '__main__':
    unittest.main()