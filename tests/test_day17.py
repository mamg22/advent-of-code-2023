import unittest

import aoc.day17 as day17

_INPUT_A = R'''
2413432311323
3215453535623
3255245654254
3446585845452
4546657867536
1438598798454
4457876987766
3637877979653
4654967986887
4564679986453
1224686865563
2546548887735
4322674655533
'''.strip()

_INPUT_B = R'''
111111111111
999999999991
999999999991
999999999991
999999999991
'''.strip()

class TestDay17(unittest.TestCase):
    def test_part_1(self):
        self.assertEqual(day17.solve_part1(_INPUT_A.splitlines()), 102)

    def test_part_2(self):
        self.assertEqual(day17.solve_part2(_INPUT_A.splitlines()), 94)

if __name__ == '__main__':
    unittest.main()