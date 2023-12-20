import unittest

import aoc.day16 as day16

_INPUT = R'''
.|...\....
|.-.\.....
.....|-...
........|.
..........
.........\
..../.\\..
.-.-/..|..
.|....-|.\
..//.|....
'''.strip()

class TestDay16(unittest.TestCase):
    def test_part_1(self):
        self.assertEqual(day16.solve_part1(_INPUT.splitlines()), 46)

    def test_part_2(self):
        self.assertEqual(day16.solve_part2(_INPUT.splitlines()), 51)

if __name__ == '__main__':
    unittest.main()