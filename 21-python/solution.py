from __future__ import annotations
import unittest
from typing import List, Union, Callable, Dict
import re
import operator


def get_input(filename: str) -> List[int]:
    with open(filename, 'r') as file:
        return file.read().splitlines()


ops = {
    '+': operator.add,
    '-': operator.sub,
    '*': operator.mul,
    '/': operator.floordiv
}

reverse_ops = {
    (operator.add, True): operator.sub,
    (operator.sub, True): operator.add,
    (operator.mul, True): operator.floordiv,
    (operator.floordiv, True): operator.mul,
    (operator.add, False): lambda c, x: c - x,
    (operator.sub, False): lambda c, x: x - c,
    (operator.mul, False): lambda c, x: c / x,
    (operator.floordiv, False): lambda c, x: x / c,
}


def build_monkeys(data):
    monkeys = {}
    for row in data:
        regex_result = re.findall(r"([a-z]{4}): ((?:[a-z]{4} [+\-*/] [a-z]{4})|(?:\d+))", row)[0]
        actions = regex_result[1].split()
        if len(actions) == 1:
            monkeys[regex_result[0]] = int(actions[0])
        else:
            monkeys[regex_result[0]] = [actions[0], actions[2], ops[actions[1]]]
    return monkeys


def run_monkey(target, done, monkeys):
    while target not in done:
        for name, (a, b, action) in monkeys.items():
            if name in done:
                continue
            if (a in done) and (b in done):
                done[name] = None if None in {done[a], done[b]} else action(done[a], done[b])


def run_monkeys(monkeys: Dict[str, Union[int, List[Union[str, Callable]]]], part: int) -> int:
    done = {}
    for name, action in dict(monkeys).items():
        if isinstance(action, int):
            done[name] = action
            del monkeys[name]
    if part != 1:
        done['humn'] = None
    first, second, _ = monkeys['root']
    run_monkey(first, done, monkeys)
    run_monkey(second, done, monkeys)
    if part == 1:
        return done['root']
    target = first if done[first] is None else second
    current = done[second] if done[first] is None else done[first]
    while target != 'humn':
        a, b, op = monkeys[target]
        target = a if done[a] is None else b
        current = reverse_ops[(op, done[a] is None)](current, done[b if done[a] is None else a])
    solution = int(current)
    return solution


class Solution(unittest.TestCase):

    def test_star_1(self):
        data = get_input('21-python/input.txt')
        print(run_monkeys(build_monkeys(data), 1))

    def test_star_2(self):
        data = get_input('21-python/input.txt')
        print(run_monkeys(build_monkeys(data), 2))


if __name__ == '__main__':
    unittest.main()
