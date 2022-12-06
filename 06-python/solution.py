import unittest
from typing import List


def get_input(filename: str) -> List[str]:
    with open(filename, 'r') as file:
        return file.read().strip()


def get_first_window_with_characters(data, size):
    for i in range(len(data) - size - 1):
        if len(set(data[i:i+size])) == size:
            return i+size


class Solution(unittest.TestCase):

    def test_star_1(self):
        data = get_input('06-python/input.txt')
        print(get_first_window_with_characters(data, 4))

    def test_star_2(self):
        data = get_input('06-python/input.txt')
        print(get_first_window_with_characters(data, 14))


if __name__ == '__main__':
    unittest.main()
