import unittest
from typing import List


def get_input(filename: str) -> List[List[int]]:
    with open(filename, 'r') as file:
        return file.read().splitlines()


def run(instructions: List[str]):
    strengths = []
    crt = []
    cycle = 1
    register = 1
    for inst in instructions:
        draw(crt, cycle, strengths, register)
        if inst == 'noop':
            cycle += 1
        else:
            cycle += 1
            draw(crt, cycle, strengths, register)
            cycle += 1
            register += int(inst[5:])
    return strengths, crt


def draw(crt, cycle, strengths, register):
    if cycle % 40 == 20:
        strengths.append(cycle * register)
    row_num = int((cycle-1)/40)
    if len(crt) <= row_num:
        crt.append([])
    row = crt[row_num]
    pixel = (cycle-1) % 40
    row.append('#' if register - 1 <= pixel <= register + 1 else '.')


class Solution(unittest.TestCase):

    def test_star_1(self):
        data = get_input('10-python/input.txt')
        print(data)
        strengths, _ = run(data)
        print(sum(strengths))

    def test_star_2(self):
        data = get_input('10-python/input.txt')
        _, crt = run(data)
        for row in crt:
            print(''.join(row))


if __name__ == '__main__':
    unittest.main()
