import unittest

import aoc.day25 as day25

_INPUT = R'''
jqt: rhn xhk nvd
rsh: frs pzl lsr
xhk: hfx
cmg: qnr nvd lhk bvb
rhn: xhk bvb hfx
bvb: xhk hfx
pzl: lsr hfx nvd
qnr: nvd
ntq: jqt hfx bvb xhk
nvd: lhk
lsr: lhk
rzs: qnr cmg lsr rsh
frs: qnr lhk lsr
'''.strip().splitlines()


class TestDay25(unittest.TestCase):
    def test_part_1(self):
        self.assertEqual(day25.solve_part1(_INPUT), 54)

if __name__ == '__main__':
    unittest.main()