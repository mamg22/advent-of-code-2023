import unittest

import aoc.day01 as day01

_PART_1_INPUT = """1abc2
pqr3stu8vwx
a1b2c3d4e5f
treb7uchet"""

_PART_2_INPUT = """two1nine
eightwothree
abcone2threexyz
xtwone3four
4nineeightseven2
zoneight234
7pqrstsixteen"""

class TestDay01(unittest.TestCase):
    def test_part_1(self):
        self.assertEqual(day01.solve_part1(_PART_1_INPUT.splitlines()), 142)

    def test_part_2(self):
        self.assertEqual(day01.solve_part2(_PART_2_INPUT.splitlines()), 281)

if __name__ == '__main__':
    unittest.main()