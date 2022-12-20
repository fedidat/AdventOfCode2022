from __future__ import annotations
import unittest
from typing import List


def get_input(filename: str) -> List[int]:
    with open(filename, 'r') as file:
        return [int(n) for n in file.read().splitlines()]


class Node:
    def __init__(self, value, prev=None, nxt=None):
        self.value = value
        self.prev: Node = prev
        self.next: Node = nxt


def build_circular_linked_list(data: List[int], key=1) -> List[Node]:
    cll = [Node(num*key) for num in data]
    for a, b in zip(cll, cll[1:]):
        a.next = b
        b.prev = a
    cll[-1].next = cll[0]
    cll[0].prev = cll[-1]
    return cll


def mix(cll: List[Node]) -> None:
    for node in cll:
        node.prev.next = node.next
        node.next.prev = node.prev
        cur_prev, cur_next = node.prev, node.next
        for _ in range(node.value % (len(cll) - 1)):
            cur_prev = cur_prev.next
            cur_next = cur_next.next
        cur_prev.next, cur_next.prev = node, node
        node.prev, node.next = cur_prev, cur_next


def grove_coords(cll: List[Node]) -> int:
    node = cll[0]
    while node.value != 0:
        node = node.next
    res = 0
    for _ in range(3):
        for _ in range(1000):
            node = node.next
        res += node.value
    return res


class Solution(unittest.TestCase):

    def test_star_1(self):
        data = get_input('20-python/input.txt')
        cll = build_circular_linked_list(data)
        mix(cll)
        print(grove_coords(cll))

    def test_star_2(self):
        data = get_input('20-python/input.txt')
        cll = build_circular_linked_list(data, 811589153)
        for _ in range(10):
            mix(cll)
        print(grove_coords(cll))


if __name__ == '__main__':
    unittest.main()
