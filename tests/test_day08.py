import unittest

import aoc.day08 as day08

_INPUT_A = """RL

AAA = (BBB, CCC)
BBB = (DDD, EEE)
CCC = (ZZZ, GGG)
DDD = (DDD, DDD)
EEE = (EEE, EEE)
GGG = (GGG, GGG)
ZZZ = (ZZZ, ZZZ)
"""

_INPUT_B = """LLR

AAA = (BBB, BBB)
BBB = (AAA, ZZZ)
ZZZ = (ZZZ, ZZZ)
"""

_INPUT_C = """LR

11A = (11B, XXX)
11B = (XXX, 11Z)
11Z = (11B, XXX)
22A = (22B, XXX)
22B = (22C, 22C)
22C = (22Z, 22Z)
22Z = (22B, 22B)
XXX = (XXX, XXX)
"""

class TestDay08(unittest.TestCase):
    def test_part_1a(self):
        self.assertEqual(day08.solve_part1(_INPUT_A.splitlines()), 2)

    def test_part_1b(self):
        self.assertEqual(day08.solve_part1(_INPUT_B.splitlines()), 6)

    def test_part_2(self):
        self.assertEqual(day08.solve_part2(_INPUT_C.splitlines()), 6)

if __name__ == '__main__':
    unittest.main()