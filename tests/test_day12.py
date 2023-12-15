import unittest

import aoc.day12 as day12

_INPUT = """???.### 1,1,3
.??..??...?##. 1,1,3
?#?#?#?#?#?#?#? 1,3,1,6
????.#...#... 4,1,1
????.######..#####. 1,6,5
?###???????? 3,2,1
"""

class TestDay12(unittest.TestCase):
    def test_part_1(self):
        self.assertEqual(day12.solve_part1(_INPUT.splitlines()), 21)

    def test_part_2(self):
        self.assertEqual(day12.solve_part2(_INPUT.splitlines()), 525152)

if __name__ == '__main__':
    unittest.main()