import unittest
from typing import Callable, List, Dict
import re
import math


class Monkey:
    items: List[int]
    fn: Callable[[int], int]
    divisible: Callable[[int], int]
    nexts: Dict[bool, int]
    inspect_count: int = 0


MONKEY_RE = re.compile(r'Monkey (\d+)')
ITEMS_RE = re.compile(r'  Starting items: .*')
OPERATION_RE = re.compile(r'  Operation: new = (.+)')
DIVISIBLE_RE = re.compile(r'  Test: divisible by (\d+)')
IF_TRUE_RE = re.compile(r'    If true: throw to monkey (\d+)')
IF_FALSE_RE = re.compile(r'    If false: throw to monkey (\d+)')


def get_input(filename: str) -> List[Monkey]:
    with open(filename, 'r') as file:
        lines = file.read().splitlines()
    monkeys: Dict[int, Monkey] = {}
    for line in lines:
        if MONKEY_RE.match(line):
            monkey_idx = int(MONKEY_RE.findall(line)[0])
            monkeys[monkey_idx] = Monkey()
            monkeys[monkey_idx].nexts = {}
        elif ITEMS_RE.match(line):
            monkeys[monkey_idx].items = [int(n)for n in re.findall(r'\d+', line)]
        elif OPERATION_RE.match(line):
            monkeys[monkey_idx].fn = lambda old, f = OPERATION_RE.findall(line)[0]: eval(f)
        elif DIVISIBLE_RE.match(line):
            monkeys[monkey_idx].divisible = int(DIVISIBLE_RE.findall(line)[0])
        elif IF_TRUE_RE.match(line):
            monkeys[monkey_idx].nexts[True] = int(IF_TRUE_RE.findall(line)[0])
        elif IF_FALSE_RE.match(line):
            monkeys[monkey_idx].nexts[False] = int(IF_FALSE_RE.findall(line)[0])
    return monkeys


def run_cycles(monkeys: Dict[int, Monkey], cycles: int, worry_divide=True):
    modulus = math.prod(m.divisible for m in monkeys.values())
    for _ in range(cycles):
        for monkey in monkeys.values():
            monkey.inspect_count += len(monkey.items)
            for item in list(monkey.items):
                next_val = int(monkey.fn(item) / 3) if worry_divide else monkey.fn(item) % modulus
                monkeys[monkey.nexts[next_val % monkey.divisible == 0]].items.append(next_val)
                monkey.items.remove(item)


class Solution(unittest.TestCase):

    def test_star_1(self):
        monkeys = get_input('11-python/input.txt')
        run_cycles(monkeys, 20)
        print(
            math.prod(sorted(m.inspect_count for m in monkeys.values())[-2:]))

    def test_star_2(self):
        monkeys = get_input('11-python/input.txt')
        run_cycles(monkeys, 10000, False)
        print(
            math.prod(sorted(m.inspect_count for m in monkeys.values())[-2:]))


if __name__ == '__main__':
    unittest.main()
