import unittest
from typing import List, Dict, Set, Tuple
import math


def get_input(filename: str) -> List[str]:
    with open(filename, 'r') as file:
        return file.read().splitlines()


def get_grid(content: List[str]) -> Tuple[Dict[Tuple[int, int], int], Dict[str, Tuple[int, int]]]:
    grid: Dict[Tuple[int, int], int] = {}
    pos: Dict[str, Tuple[int, int]] = {}
    for y_coord, line in enumerate(reversed(content)):
        for x_coord, char in enumerate(line):
            grid[(x_coord, y_coord)] = 0 if char == 'S' else 25 if char == 'E' else ord(char) - ord('a')
            if char in ['S', 'E']:
                pos[char] = (x_coord, y_coord)
    return grid, pos


def distances_from_end(grid, pos) -> int:
    dist: Dict[Tuple[int, int], int] = {}
    q: List[Tuple[int, int]] = [pos.get('E')]
    dist[pos.get('E')]: int = 0
    visited: Set[Tuple[int, int]] = set()
    while q:
        cur = q.pop()
        for x_off, y_off in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            adj = (cur[0]+x_off, cur[1]+y_off)
            if adj in grid and (cur, adj) not in visited and grid[cur] <= grid[adj] + 1:
                visited.add((cur, adj))
                q.insert(0, adj)
                dist[adj] = min(dist.get(adj, math.inf), dist[cur] + 1)
    return dist


class Solution(unittest.TestCase):

    def test_star_1(self):
        data = get_input('12-python/input.txt')
        grid, pos = get_grid(data)
        print(distances_from_end(grid, pos)[pos.get('S')])

    def test_star_2(self):
        data = get_input('12-python/input.txt')
        grid, pos = get_grid(data)
        dist = distances_from_end(grid, pos)
        print(min(dist[k] for (k, v) in grid.items() if v == 0 and k in dist))


if __name__ == '__main__':
    unittest.main()
