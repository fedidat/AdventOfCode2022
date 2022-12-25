from __future__ import annotations
import unittest
from typing import List


def get_input(filename: str) -> List[str]:
    with open(filename, 'r') as file:
        return file.read().splitlines()


DIGITS = {'=': -2, '-': -1, '0': 0, '1': 1, '2': 2}


def to_base10(snafu: str) -> int:
    return sum(DIGITS[snaf] * (5 ** i) for i, snaf in enumerate(snafu[::-1]))


def to_snafu(base10: int) -> str:
    output = ''
    while base10:
        output = '012=-'[base10 % 5] + output
        base10 = (base10 + 2) // 5
    return output


class Solution(unittest.TestCase):

    def test_star_1(self):
        #data = get_input('25-python/example-1.txt')
        #print(sum(snafu_to_base10(snafu) for snafu in data))
        #data = get_input('25-python/example-2.txt')
        #print([base10_to_snafu(int(b10)) for b10 in data])
        data = get_input('25-python/input.txt')
        print(to_snafu(sum(to_base10(snafu) for snafu in data)))

    def test_star_2(self):
        print("Happy new year :)")


if __name__ == '__main__':
    unittest.main()
