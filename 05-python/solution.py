import unittest
from typing import List
import re


def get_input(filename: str) -> List[str]:
    with open(filename, 'r') as file:
        (config_lines, instructions_lines) = [
            g.splitlines() for g in file.read().split('\n\n')]
        config = [[] for x in range(int(len(config_lines[0]) / 4 + 1))]
        for i in list(reversed(range(len(config_lines)-1))):
            for idx, j in enumerate(range(1, len(config_lines[0]), 4)):
                if config_lines[i][j] != ' ':
                    config[idx].append(config_lines[i][j])
        instructions = []
        match_nums = re.compile(r'\d+')
        for line in instructions_lines:
            (num, src, dst) = [(int(n)) for n in match_nums.findall(line)]
            instructions.append([num, src-1, dst-1])
        return (config, instructions)


def move_one_by_one(config, inst):
    for _ in range(inst[0]):
        config[inst[2]].append(config[inst[1]].pop())


def move_at_once(config, inst):
    cutpoint = len(config[inst[1]])-inst[0]
    config[inst[2]] += config[inst[1]][cutpoint:]
    config[inst[1]] = config[inst[1]][0:cutpoint]


def execute(config, instructions, stack):
    for inst in instructions:
        _ = move_one_by_one(
            config, inst) if stack else move_at_once(config, inst)


class Solution(unittest.TestCase):

    def test_star_1(self):
        config, instructions = get_input('05-python/input.txt')
        execute(config, instructions, True)
        print(''.join([stack[len(stack)-1] for stack in config]))

    def test_star_2(self):
        config, instructions = get_input('05-python/input.txt')
        execute(config, instructions, False)
        print(''.join([stack[len(stack)-1] for stack in config]))


if __name__ == '__main__':
    unittest.main()
