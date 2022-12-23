from __future__ import annotations
import unittest
from typing import List, Set, Tuple
from collections import defaultdict


def get_input(filename: str) -> List[int]:
    with open(filename, 'r') as file:
        lines = file.read().splitlines()
        return {(y, x) for y, line in enumerate(lines) for x, char in enumerate(line) if char == '#'}


OFFSETS = {
    'N': (-1, 0), 'S': (1, 0), 'E': (0, 1), 'W': (0, -1),
    'NW': (-1, -1), 'NE': (-1, 1), 'SW': (1, -1), 'SE': (1, 1)}

PROPOSALS = [('N', 'NE', 'NW'), ('S', 'SE', 'SW'), ('W', 'NW', 'SW'), ('E', 'NE', 'SE')]


def add(pt1, pt2):
    return (pt1[0]+pt2[0], pt1[1]+pt2[1])


def propose(grid, point, cycle):
    if not any(add(point, offset) in grid for offset in OFFSETS.values()):
        return None
    for i in range(4):
        proposal = PROPOSALS[(cycle + i) % 4]
        if not any(add(point, OFFSETS[prop]) in grid for prop in proposal):
            return proposal[0]
    return None


def run(grid: Set[Tuple[int, int]], part: int, cycles: int):
    for cycle in range(cycles):
        moved = False
        props = defaultdict(list)
        for point in grid:
            prop = propose(grid, point, cycle)
            if prop is not None:
                props[add(point, OFFSETS[prop])].append(point)
        for prop, origins in props.items():
            if len(origins) == 1:
                moved = True
                grid.remove(origins[0])
                grid.add(prop)
        if part == 2 and not moved:
            return cycle + 1
    min_y, max_y = min(y for y, _ in grid), max(y for y, _ in grid)
    min_x, max_x = min(x for _, x in grid), max(x for _, x in grid)
    return (max_y - min_y + 1) * (max_x - min_x + 1) - len(grid)


class Solution(unittest.TestCase):

    def test_star_1(self):
        grid = get_input('23-python/input.txt')
        print(run(grid, 1, 10))

    def test_star_2(self):
        grid = get_input('23-python/input.txt')
        print(run(grid, 2, 10000))


if __name__ == '__main__':
    unittest.main()
