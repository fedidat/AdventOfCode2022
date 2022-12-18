import unittest
from typing import List, Tuple
from collections import deque
import math


def get_input(filename: str) -> List[Tuple[int, int, int, int]]:
    with open(filename, 'r') as file:
        return {tuple(int(n) for n in line.split(',')) for line in file.read().splitlines()}


def get_adj(cube):
    adj = set()
    for dim in range(3):
        for dim_off in (-1, 1):
            off_point = list(cube)
            off_point[dim] += dim_off
            adj.add(tuple(off_point))
    return adj


def surface(grid):
    adj = {}
    for cube in grid:
        adj[cube] = sum(adj in grid for adj in get_adj(cube))
    return sum(6-n for n in adj.values())


OUTSIDE = set()
INSIDE = set()


def reaches_outside(grid, cube, max_cubes):
    if cube in OUTSIDE:
        return True
    if cube in INSIDE:
        return False
    seen = set()
    to_visit = deque([cube])
    while to_visit:
        cube = to_visit.popleft()
        if cube in grid or cube in seen:
            continue
        seen.add(cube)
        if len(seen) > max_cubes:
            # after propagating to all possible cubes, all non seen cubes considered outside
            for p in seen:
                OUTSIDE.add(p)
            return True
        for adj in get_adj(cube):
            to_visit.append(adj)
    for p in seen:
        INSIDE.add(p)
    return False


def surface_without_bubbles(grid):
    max_cubes = math.prod(max(cube[d] for cube in grid) for d in range(3))
    total = 0
    for cube in grid:
        for adj in get_adj(cube):
            if reaches_outside(grid, adj, max_cubes):
                total += 1
    return total


class Solution(unittest.TestCase):

    def test_star_1(self):
        data = get_input('18-python/input.txt')
        print(surface(data))

    def test_star_2(self):
        data = get_input('18-python/input.txt')
        print(surface_without_bubbles(data))


if __name__ == '__main__':
    unittest.main()
