import unittest

import aoc.day22 as day22

_INPUT = R'''
1,0,1~1,2,1
0,0,2~2,0,2
0,2,3~2,2,3
0,0,4~0,2,4
2,0,5~2,2,5
0,1,6~2,1,6
1,1,8~1,1,9
'''.strip().splitlines()

# 666
# 875
# 445
# .32
# .11

_CUSTOM_INPUT = R'''
1,0,1~2,0,1
1,0,2~1,0,2
2,0,2~2,0,2
0,0,3~1,0,3
2,0,3~2,0,4
0,0,5~2,0,5
1,0,4~1,0,4
0,0,4~0,0,4
'''.strip().splitlines()


class TestDay22(unittest.TestCase):
    def test_part_1(self):
        self.assertEqual(day22.solve_part1(_INPUT), 5)

    def test_part_1custom(self):
        self.assertEqual(day22.solve_part1(_CUSTOM_INPUT), 4)

    def test_part_2(self):
        self.assertEqual(day22.solve_part2(_INPUT), 7)

    def test_part_2custom(self):
        self.assertEqual(day22.solve_part2(_CUSTOM_INPUT), 13)

if __name__ == '__main__':
    unittest.main()