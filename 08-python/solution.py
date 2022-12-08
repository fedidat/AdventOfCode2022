import unittest
from typing import List


def get_input(filename: str) -> List[List[int]]:
    with open(filename, 'r') as file:
        return [[int(n) for n in l] for l in file.read().splitlines()]


def get_visible(grid: List[List[int]]) -> int:
    vis1 = [[False] * len(grid[0]) for i in range(len(grid))]
    for x in range(0, len(grid[0]), 1):
        maxh = 0
        for y in range(0, len(grid), 1):  # top to bottom
            vis1[y][x] = vis1[y][x] or y == 0 or maxh < grid[y][x]
            maxh = max(maxh, grid[y][x])
    vis2 = [[False] * len(grid[0]) for i in range(len(grid))]
    for x in range(0, len(grid[0]), 1):
        maxh = 0
        for y in range(len(grid)-1, -1, -1):  # bottom to top
            vis2[y][x] = vis2[y][x] or y == len(grid)-1 or maxh < grid[y][x]
            maxh = max(maxh, grid[y][x])
    vis3 = [[False] * len(grid[0]) for i in range(len(grid))]
    for y in range(0, len(grid), 1):  # left to right
        maxh = 0
        for x in range(0, len(grid[y]), 1):
            vis3[y][x] = vis3[y][x] or x == 0 or maxh < grid[y][x]
            maxh = max(maxh, grid[y][x])
    vis4 = [[False] * len(grid[0]) for i in range(len(grid))]
    for y in range(0, len(grid), 1):  # right to left
        maxh = 0
        for x in range(len(grid[y])-1, -1, -1):
            vis4[y][x] = vis4[y][x] or x == len(grid[y])-1 or maxh < grid[y][x]
            maxh = max(maxh, grid[y][x])
    visible = [[False] * len(grid[0]) for i in range(len(grid))]
    for y in range(0, len(grid), 1):  # combine all 4 directions
        for x in range(0, len(grid[y]), 1):
            visible[y][x] = vis1[y][x] or vis2[y][x] or vis3[y][x] or vis4[y][x]
    return sum(sum(l) for l in visible)


def best_scenic_score(grid: List[List[int]]) -> int:
    scenic_score = 0
    for y0, l0 in enumerate(grid):
        for x0, c0 in enumerate(l0):
            counter_b = 0
            for y in range(y0+1, len(grid)):  # to the bottom
                counter_b += 1
                if grid[y][x0] >= c0:
                    break
            counter_t = 0
            for y in range(y0-1, -1, -1):  # to the top
                counter_t += 1
                if grid[y][x0] >= c0:
                    break
            counter_r = 0
            for x in range(x0+1, len(l0)):  # to the right
                counter_r += 1
                if l0[x] >= c0:
                    break
            counter_l = 0
            for x in range(x0-1, -1, -1):  # to the left
                counter_l += 1
                if l0[x] >= c0:
                    break
            scenic_score = max(scenic_score, counter_b *
                               counter_t * counter_r * counter_l)
    return scenic_score


class Solution(unittest.TestCase):

    def test_star_1(self):
        data = get_input('08-python/input.txt')
        print(get_visible(data))

    def test_star_2(self):
        data = get_input('08-python/input.txt')
        print(best_scenic_score(data))


if __name__ == '__main__':
    unittest.main()
