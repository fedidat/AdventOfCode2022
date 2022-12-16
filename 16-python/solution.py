import unittest
from typing import List, Tuple
import re


def get_input(filename: str) -> List[Tuple[int, int, int, int]]:
    p = re.compile(r"Valve (\w+) has flow rate=(\d+); tunnels? leads? to valves? ((?:\w+(?:, )?)+)")
    with open(filename, 'r') as file:
        result = [p.findall(l)[0] for l in file.read().splitlines()]
        return {a: (int(b), c.split(', ')) for a, b, c in result}


def max_pressure(valves, cur, time_limit, time, flow, visited, opened):
    if time == time_limit:
        return sum(flow)
    if (time, cur) in visited and visited[(time, cur)] >= sum(flow):
        return 0
    visited[time, cur] = sum(flow)
    if all(valves[k][0] > 0 for k in valves.keys()):
        return max_pressure(valves, cur, time_limit, time+1, flow+[sum(valves[k][0] for k in opened)], visited, opened)
    best = 0
    if not cur in opened and valves[cur][0] > 0:
        opened.add(cur)
        best = max(best, max_pressure(valves, cur, time_limit, time+1, flow+[sum(valves[k][0] for k in opened)], visited, opened))
        opened.remove(cur)
    rates = sum(valves[k][0] for k in opened)
    for adj in valves[cur][1]:
        best = max(best, max_pressure(valves, adj, time_limit, time+1, flow+[rates], visited, opened))
    return best


def max_with_pair(valves, cur1, cur2, time_limit, time, flow, visited, opened):
    if time == time_limit:
        return sum(flow)
    if (time, cur1, cur2) in visited and visited[(time, cur1, cur2)] >= sum(flow):
        return 0
    visited[time, cur1, cur2] = sum(flow)
    if all(v for k, v in opened.items() if valves[k][0] > 0):
        return max_with_pair(valves, cur1, cur2, time_limit, time+1, flow+[sum(valves[k][0] for k,v in opened.items() if v)], visited, opened)
    best = 0
    if not opened[cur1] and valves[cur1][0] > 0:
        opened[cur1] = True
        if not opened[cur2] and valves[cur2][0] > 0:
            opened[cur2] = True
            best = max(best, max_with_pair(valves, cur1, cur2, time_limit, time+1, flow+[sum(valves[k][0] for k,v in opened.items() if v)], visited, opened))
            opened[cur2] = False
        rates = sum(valves[k][0] for k,v in opened.items() if v)
        for adj2 in valves[cur2][1]:
            best = max(best, max_with_pair(valves, cur1, adj2, time_limit, time+1, flow+[rates], visited, opened))
        opened[cur1] = False
    rates = sum(valves[k][0] for k,v in opened.items() if v)
    for adj1 in valves[cur1][1]:
        if not opened[cur2] and valves[cur2][0] > 0:
            opened[cur2] = True
            best = max(best, max_with_pair(valves, adj1, cur2, time_limit, time+1, flow+[sum(valves[k][0] for k,v in opened.items() if v)], visited, opened))
            opened[cur2] = False
        for adj2 in valves[cur2][1]:
            best = max(best, max_with_pair(valves, adj1, adj2, time_limit, time+1, flow+[rates], visited, opened))
    return best


class Solution(unittest.TestCase):

    def test_star_1(self):
        data = get_input('16-python/input.txt')
        print(max_pressure(data, 'AA', 30, 1, [0], {}, set()))

    def test_star_2(self):
        data = get_input('16-python/input.txt')
        print(max_with_pair(data, 'AA', 'AA', 26, 1, [0], {}, {k: False for k in data.keys()}))


if __name__ == '__main__':
    unittest.main()
