import unittest
from typing import List, Tuple


def get_input(filename: str) -> List[Tuple[int, int, int, int]]:
    with open(filename, 'r') as file:
        return file.read().strip()


SHAPES = [
    {(0, 0), (0, 1), (0, 2), (0, 3)},
    {(0, 1), (1, 0), (1, 1), (1, 2), (2, 1)},
    {(0, 0), (0, 1), (0, 2), (1, 2), (2, 2)},
    {(0, 0), (1, 0), (2, 0), (3, 0)},
    {(0, 0), (0, 1), (1, 0), (1, 1)},
]


def is_busy_down(grid, shape):
    return any(y == 0 for (y, _) in shape) or any((y-1, x) in grid for (y, x) in shape)


def move(grid, shape, direction):
    shape = {(y-1, x) for (y, x) in shape}
    if direction == '>' and not (any(x == WIDTH-1 for (_, x) in shape) or any((y, x+1) in grid for (y, x) in shape)):
        shape = {(y, x+1) for (y, x) in shape}
    if direction == '<' and not (any(x == 0 for (_, x) in shape) or any((y, x-1) in grid for (y, x) in shape)):
        shape = {(y, x-1) for (y, x) in shape}
    return shape


def grid_height(grid):
    return (max(y for (y, _) in grid)+1)-2 if grid else -2


WIDTH = 7
KEEP_BACK = 50


def simulate(directions, rocks):
    grid, seen, shape_idx, cycle = {}, {}, 0, 0
    while shape_idx <= rocks:
        shape_base = grid_height(grid) + 5
        shape = {(y+shape_base+1, x+2) for (y, x) in SHAPES[shape_idx % len(SHAPES)]}
        while not is_busy_down(grid, shape):
            shape = move(grid, shape, directions[cycle])
            cycle = (cycle + 1) % len(directions)
            if shape_idx % KEEP_BACK == 0:  # clean up periodically
                grid = {(y, x) for (y, x) in grid if y > shape_base - KEEP_BACK}
        grid.update(shape)
        max_y = max([y for (y, _) in grid])
        key = (cycle, frozenset([(max_y-y, x) for (y, x) in grid if max_y-y <= KEEP_BACK]))
        if key in seen:  # state seen, skip as much as possible towards goal and continue
            height_since_last = grid_height(grid) - seen[key][0]
            shapes_since_last = shape_idx - seen[key][1]
            shapes_left = rocks - shape_idx
            jumps_possible = int(shapes_left / shapes_since_last)
            height_diff = height_since_last * jumps_possible
            grid = {(y+height_diff, x) for (y, x) in grid}
            shape = {(y+height_diff, x) for (y, x) in shape}
            shape_idx = shape_idx + jumps_possible * shapes_since_last
        seen[key] = (grid_height(grid)-1, shape_idx)
        shape_idx += 1
    return grid_height(grid)


class Solution(unittest.TestCase):

    def test_star_1(self):
        data = get_input('17-python/input.txt')
        print(simulate(data, 2022))

    def test_star_2(self):
        data = get_input('17-python/input.txt')
        print(simulate(data, 1000000000000))


if __name__ == '__main__':
    unittest.main()
