import unittest
from typing import List, Tuple, Dict
import re


def get_input(filename: str) -> List[Tuple[int, int, int, int]]:
    with open(filename, 'r') as file:
        return [tuple(int(n) for n in re.findall(r"(-?\d+)", s)) for s in file.read().splitlines()]


def manhattan(a: Tuple[int, int], b: Tuple[int, int]) -> int:
    return abs(b[0] - a[0]) + abs(b[1] - a[1])


def covered_in_row(data: List[Tuple[int, int, int, int]], row: int) -> int:
    intervals = []
    for a, b, c, d in data:  # add all intervals covered by each sensor in the row
        beacon_dist = manhattan((a, b), (c, d))
        dist_to_row = abs(b - row)
        left_to_spend = beacon_dist - dist_to_row
        if left_to_spend > 0:
            intervals.append([a - left_to_spend, a + left_to_spend])
    intervals.sort()  # now merge intervals
    merged = [intervals[0]]
    for a, b in sorted(intervals[1:]):
        if merged[-1][0] <= a <= merged[-1][1]:
            merged[-1][1] = max(merged[-1][1], b)
        else:
            merged.append((a, b))
    # return total number of covered tiles
    return sum(b - a for a, b in merged)


def find_uncovered(data: List[Tuple[int, int, int, int]], max_xy: int) -> int:
    incs = set()
    decs = set()
    for a, b, c, d in data:  # add all lines outside radius
        beacon_dist = manhattan((a, b), (c, d))
        # y = -x + r + 1 (increasing above sensor)
        incs.add(b + a + beacon_dist + 1)
        # y = -x + r + 1 (increasing under sensor)
        incs.add(b + a - beacon_dist + 1)
        # y = -x + r + 1 (decreasing above sensor)
        decs.add(b - a + beacon_dist + 1)
        # y = -x + r + 1 (decreasing under sensor)
        decs.add(b - a - beacon_dist + 1)
    for inc in incs:  # look for intersections between increasing and decreasing curves not in distance of any sensor
        for dec in decs:
            intersec = ((inc-dec)//2, (inc+dec)//2)
            if 0 < intersec[0] < max_xy and 0 < intersec[1] < max_xy:
                if not any(manhattan(intersec, (a, b)) < manhattan((a, b), (c, d)) for (a, b, c, d) in data):
                    return max_xy * intersec[0] + intersec[1]
    return None


class Solution(unittest.TestCase):

    def test_star_1(self):
        data = get_input('15-python/input.txt')
        print(covered_in_row(data, 2000000))

    def test_star_2(self):
        data = get_input('15-python/input.txt')
        print(find_uncovered(data, 4000000))


if __name__ == '__main__':
    unittest.main()
