import unittest
from typing import List, Optional, Tuple
import math
import itertools


def get_input(filename: str) -> List[Tuple[any, any]]:
    with open(filename, 'r') as file:
        return file.read().splitlines()


def right_order_pair(left, right) -> Optional[bool]:
    if isinstance(left, int) and isinstance(right, int):
        if left == right:
            return None
        return left < right
    elif isinstance(left, int):
        return right_order_pair([left], right)
    elif isinstance(right, int):
        return right_order_pair(left, [right])
    else:
        for left_element, right_element in itertools.zip_longest(left, right):
            if left_element is None:
                return True
            if right_element is None:
                return False
            result = right_order_pair(left_element, right_element)
            if result is not None:
                return result
    return None


def right_order_pairs(pairs) -> int:
    total = 0
    for i, (left, right) in enumerate(pairs):
        if right_order_pair(left, right):
            total += i + 1
    return total


def reorder(elements) -> List[any]:
    result = []
    for a in elements:
        i = 0
        while i < len(result):
            if right_order_pair(a, result[i]):
                break
            i += 1
        result.insert(i, a)
    return result


class Solution(unittest.TestCase):

    def test_star_1(self):
        data = get_input('13-python/input.txt')
        print(right_order_pairs([(eval(x), eval(y))
              for x, y, _ in zip(*[iter(data + [""])]*3)]))

    def test_star_2(self):
        data = get_input('13-python/input.txt')
        dividers = [[[2]], [[6]]]
        result = reorder([eval(line) for line in data if line != ""]+dividers)
        print(math.prod(result.index(divider)+1 for divider in dividers))


if __name__ == '__main__':
    unittest.main()
