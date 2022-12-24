from __future__ import annotations
import unittest
from typing import List, Tuple, Set, Union

OFFSETS = {'>': (1, 0), '<': (-1, 0), 'v': (0, 1), '^': (0, -1), '': (0, 0)}


def get_input(filename: str) -> Union[Set[Tuple[int, int]], Set[Tuple[int, int, Tuple[int, int]]]]:
    walls = set()
    blizzards = set()
    with open(filename, 'r') as file:
        lines = file.read().splitlines()
        for y, line in enumerate(lines):
            for x, char in enumerate(line):
                if char == '#':
                    walls.add((x-1, y-1))
                elif char in OFFSETS:
                    blizzards.add((x-1, y-1, OFFSETS[char]))
    return walls, blizzards


def solve(walls: Set[Tuple[int, int]], blizzards: List[Tuple[int, int, Tuple[int, int]]], part: int):
    max_x, max_y = max(x for x, _ in walls), max(y for _, y in walls)
    start, goal = (0, -1), (max_x-1, max_y)
    walls |= {(x, -2) for x in range(start[0]-1, start[0]+2)}  # wall off entry
    walls |= {(x, max_y+1) for x in range(goal[0]-1, goal[0]+2)}  # wall off exit
    goals = [goal] if part == 1 else [goal, start, goal]  # part 2 goes to goal then start then goal

    step = 0
    bfs_queue = {start}
    while goals:
        step += 1
        next_positions = {(px+dx, py+dy) for dx, dy in OFFSETS.values() for px, py in bfs_queue}
        next_blizzards = {((px+step*dx) % max_x, (py+step*dy) % max_y) for px, py, (dx, dy) in blizzards}
        bfs_queue = {goals.pop(0)} if goals[0] in bfs_queue else next_positions - next_blizzards - walls
    return step-1


class Solution(unittest.TestCase):

    def test_star_1(self):
        walls, blizzards = get_input('24-python/input.txt')
        print(solve(walls, blizzards, 1))

    def test_star_2(self):
        walls, blizzards = get_input('24-python/input.txt')
        print(solve(walls, blizzards, 2))


if __name__ == '__main__':
    unittest.main()
