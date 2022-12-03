import unittest
from typing import List


def get_input(filename: str) -> List[str]:
    with open(filename, 'r') as file:
        return file.read().splitlines()


def get_shared_item(sack: str) -> str:
    return next(s for s in sack[:int(len(sack)/2)] if s in sack[int(len(sack)/2):])


def get_badge(sacks: List[str]) -> str:
    return next(i for i in sacks[0] if i in sacks[1] and i in sacks[2])


def get_item_priority(item: str) -> int:
    base = ord('A') - 26 if item.isupper() else ord('a')
    return ord(item) - base + 1


class Solution(unittest.TestCase):

    def test_star_1(self):
        data = get_input('03-python/input.txt')
        total = sum(get_item_priority(get_shared_item(sack)) for sack in data)
        print(total)

    def test_star_2(self):
        data = get_input('03-python/input.txt')
        total = sum(get_item_priority(
            get_badge(data[i: i+3])) for i in range(0, len(data), 3))
        print(total)


if __name__ == '__main__':
    unittest.main()
