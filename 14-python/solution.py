import unittest
from typing import List, Tuple, Dict


def get_input(filename: str) -> List[List[Tuple[int, int]]]:
    with open(filename, 'r') as file:
        return [[tuple(int(c) for c in s.strip().split(',')) for s in s.split('->')] for s in file.read().splitlines()]


def get_grid(data: List[List[Tuple[int, int]]]) -> Dict[Tuple[int, int], str]:
    grid: Dict[Tuple[int, int], str] = {}
    for path in data:
        for pt_a, pt_b in zip(path, path[1:]):
            if pt_a[0] == pt_b[0]:  # same x, vertical
                for y in range(min(pt_a[1], pt_b[1]), max(pt_a[1], pt_b[1]) + 1):
                    grid[(pt_a[0], y)] = '#'
            else:  # horizontal
                for x in range(min(pt_a[0], pt_b[0]), max(pt_a[0], pt_b[0]) + 1):
                    grid[(x, pt_a[1])] = '#'
    return grid


def print_grid(grid: Dict[Tuple[int, int], str]):
    min_x = min(pt[0] for pt in grid.keys())
    max_x = max(pt[0] for pt in grid.keys())
    min_y = min(pt[1] for pt in grid.keys())
    max_y = max(pt[1] for pt in grid.keys())
    for y in range(min_y, max_y+1):
        for x in range(min_x, max_x+1):
            if (x, y) in grid:
                print(grid[(x, y)], end="")
            else:
                print('.', end="")
        print()


def get_wiggle_room(grid, pt):
    if (pt[0], pt[1]+1) not in grid:
        return (pt[0], pt[1]+1)
    elif (pt[0]-1, pt[1]+1) not in grid:
        return (pt[0]-1, pt[1]+1)
    elif (pt[0]+1, pt[1]+1) not in grid:
        return (pt[0]+1, pt[1]+1)
    return None


def drop_sand(grid: Dict[Tuple[int, int], str], origin: Tuple[int, int], part: int) -> int:
    max_y = max(pt[1] for pt in grid.keys())
    floor = max_y + 2
    for cycle in range(100000):
        pt = origin
        while (wiggle := get_wiggle_room(grid, pt)) is not None:
            if part == 1 and wiggle[1] > max_y:  # will fall forever
                return cycle
            if part == 2 and wiggle[1] == floor-1:  # got to ground
                break
            pt = wiggle
        if part == 2 and pt == origin:  # reached ceiling
            return cycle+1
        grid[pt] = 'o'


class Solution(unittest.TestCase):

    def test_star_1(self):
        data = get_input('14-python/input.txt')
        grid = get_grid(data)
        print(drop_sand(grid, (500, 0), 1))

    def test_star_2(self):
        data = get_input('14-python/input.txt')
        grid = get_grid(data)
        print(drop_sand(grid, (500, 0), 2))


if __name__ == '__main__':
    unittest.main()
