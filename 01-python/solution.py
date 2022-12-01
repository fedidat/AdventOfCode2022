import unittest
import heapq

def get_input(filename):
    with open(filename, 'r') as file:
        return [[int(x) for x in s.splitlines()] for s in file.read().split('\n\n')]


class Solution(unittest.TestCase):

    def test_star_1(self):
        data = get_input('01-python/input.txt')
        sum_top_elf = sum(max(data, key=sum))
        print(sum_top_elf)

    def test_star_2(self):
        data = get_input('01-python/input.txt')
        sum_top_3_elves = sum(sum(elf) for elf in heapq.nlargest(3, data, key=sum))   
        print(sum_top_3_elves)


if __name__ == '__main__':
    unittest.main()
