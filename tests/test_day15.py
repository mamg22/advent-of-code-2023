import unittest

import aoc.day15 as day15

_INPUT = """
rn=1,cm-,qp=3,cm=2,qp-,pc=4,ot=9,ab=5,pc-,pc=6,ot=7
""".strip()

class TestDay15(unittest.TestCase):
    def test_part_1(self):
        self.assertEqual(day15.solve_part1(_INPUT.splitlines()), 1320)

    def test_part_2(self):
        self.assertEqual(day15.solve_part2(_INPUT.splitlines()), 145)

if __name__ == '__main__':
    unittest.main()