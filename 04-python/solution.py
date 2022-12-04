import unittest
from typing import List


def get_input(filename: str) -> List[str]:
    with open(filename, 'r') as file:
        return [[[int(n) for n in h.split('-')] for h in l.split(',')] for l in file.read().splitlines()]


def is_contained(a, b):
    return a[0] <= b[0] and a[1] >= b[1]


def is_either_contained(a, b):
    return is_contained(a, b) or is_contained(b, a)  # pylint: disable=W1114


def is_overlap(a, b):
    return (a[0] >= b[0] and a[0] <= b[1]) or (
        a[1] >= b[0] and a[1] <= b[1]) or is_contained(a, b)


class Solution(unittest.TestCase):

    def test_star_1(self):
        data = get_input('04-python/input.txt')
        print(sum(is_either_contained(a, b) for (a, b) in data))

    def test_star_2(self):
        data = get_input('04-python/input.txt')
        print(sum(is_overlap(a, b) for (a, b) in data))


if __name__ == '__main__':
    unittest.main()
