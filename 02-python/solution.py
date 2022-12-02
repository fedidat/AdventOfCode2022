import unittest
import heapq

def get_input(filename):
    with open(filename, 'r') as file:
        return [s.split(' ') for s in file.read().splitlines()]

def round_score(a, b):
    score = 3 * ((2 * a + b + 1) % 3)
    return score + b + 1

def play_score(a, b):
    score = b * 3
    chosen_card = (a + b - 1) % 3
    return score + chosen_card + 1


class Solution(unittest.TestCase):

    def test_star_1(self):
        data = get_input('02-python/input.txt')
        total = sum(round_score('ABC'.index(a), 'XYZ'.index(b)) for (a, b) in data)
        print(total)

    def test_star_2(self):
        data = get_input('02-python/input.txt')
        total = sum(play_score('ABC'.index(a), 'XYZ'.index(b)) for (a, b) in data)
        print(total)


if __name__ == '__main__':
    unittest.main()
