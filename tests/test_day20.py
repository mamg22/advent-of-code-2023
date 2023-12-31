import unittest

import aoc.day20 as day20

_INPUT_A = R'''
broadcaster -> a, b, c
%a -> b
%b -> c
%c -> inv
&inv -> a
'''.strip().splitlines()

_INPUT_B = R'''
broadcaster -> a
%a -> inv, con
&inv -> b
%b -> con
&con -> output
'''.strip().splitlines()


class TestDay20(unittest.TestCase):
    def test_part_1a(self):
        self.assertEqual(day20.solve_part1(_INPUT_A), 32000000)

    def test_part_1b(self):
        self.assertEqual(day20.solve_part1(_INPUT_B), 11687500)


if __name__ == '__main__':
    unittest.main()