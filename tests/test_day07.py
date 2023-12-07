import unittest

import aoc.day07 as day07

_INPUT = """32T3K 765
T55J5 684
KK677 28
KTJJT 220
QQQJA 483
"""

_ALT_INPUT = """2345A 1
Q2KJJ 13
Q2Q2Q 19
T3T3J 17
T3Q33 11
2345J 3
J345A 2
32T3K 5
T55J5 29
KK677 7
KTJJT 34
QQQJA 31
JJJJJ 37
JAAAA 43
AAAAJ 59
AAAAA 61
2AAAA 23
2JJJJ 53
JJJJ2 41
"""

class TestDay07(unittest.TestCase):
    def test_part_1(self):
        self.assertEqual(day07.solve_part1(_INPUT.splitlines()), 6440)

    def test_part_1_alt(self):
        self.assertEqual(day07.solve_part1(_ALT_INPUT.splitlines()), 6592)

    def test_part_2(self):
        self.assertEqual(day07.solve_part2(_INPUT.splitlines()), 5905)

    def test_part_2_alt(self):
        self.assertEqual(day07.solve_part2(_ALT_INPUT.splitlines()), 6839)

if __name__ == '__main__':
    unittest.main()