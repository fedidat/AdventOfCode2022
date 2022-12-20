from __future__ import annotations
import unittest
from typing import List, Tuple
import re
import math


def get_input(filename: str) -> List[Tuple[int, int, int, int]]:
    blueprint_re = r"Blueprint (\d+):(?:\n )? Each ore robot costs (\d+) ore.(?:\n )? Each clay robot costs (\d+) ore.(?:\n )? Each obsidian robot costs (\d+) ore and (\d+) clay.(?:\n )? Each geode robot costs (\d+) ore and (\d+) obsidian."
    with open(filename, 'r') as file:
        return [[int(n) for n in line] for line in re.findall(blueprint_re, file.read(), re.MULTILINE)]


def dfs(time, goal, bots, res, costs, max_ore_cost, prune):
    global m
    if (goal == 0 and bots[0] >= max_ore_cost
        or goal == 1 and bots[1] >= costs[2][1]
        or goal == 2 and (bots[2] >= costs[3][2] or bots[1] == 0)
        or goal == 3 and bots[2] == 0
        or res[3] + bots[3] * time + prune[time] <= m):
        return
    while time:
        bots_n = list(bots)
        if goal == 0 and res[0] >= costs[0][0]:
            res_n = [v-costs[goal][k]+bots[k] for k, v in enumerate(res)]
            bots_n[goal] += 1
            for goal in range(4):
                dfs(time - 1, goal, bots_n, res_n, costs, max_ore_cost, prune)
            return
        elif goal == 1 and res[0] >= costs[1][0]:
            res_n = [v-costs[goal][k]+bots[k] for k, v in enumerate(res)]
            bots_n[goal] += 1
            for goal in range(4):
                dfs(time - 1, goal, bots_n, res_n, costs, max_ore_cost, prune)
            return
        elif goal == 2 and res[0] >= costs[2][0] and res[1] >= costs[2][1]:
            res_n = [v-costs[goal][k]+bots[k] for k, v in enumerate(res)]
            bots_n[goal] += 1
            for goal in range(4):
                dfs(time - 1, goal, bots_n, res_n, costs, max_ore_cost, prune)
            return
        elif goal == 3 and res[0] >= costs[3][0] and res[2] >= costs[3][2]:
            res_n = [v-costs[goal][k]+bots[k] for k, v in enumerate(res)]
            bots_n[goal] += 1
            for goal in range(4):
                dfs(time - 1, goal, bots_n, res_n, costs, max_ore_cost, prune)
            return
        time -= 1
        res = [v+bots[k] for k, v in enumerate(res)]
    m = max(m, res[3])


def quality(bp, time):
    global m
    m = 0
    prune = [(time - 1) * time // 2 for time in range(time + 1)]
    costs = [[bp[1], 0, 0, 0], [bp[2], 0, 0, 0], [bp[3], bp[4], 0, 0], [bp[5], 0, bp[6], 0]]
    for g in range(4):
        dfs(time, g, [1, 0, 0, 0], [0, 0, 0, 0], costs, max(k[0] for k in costs), prune)
    return m


class Solution(unittest.TestCase):

    def test_star_1(self):
        data = get_input('19-python/input.txt')
        print(sum(quality(d, 24)*d[0] for d in data))

    def test_star_2(self):
        data = get_input('19-python/input.txt')
        print(math.prod(quality(d, 32) for d in data[:3]))


if __name__ == '__main__':
    unittest.main()
