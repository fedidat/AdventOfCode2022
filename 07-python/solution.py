import unittest
from typing import List, Dict
import re


def get_input(filename: str) -> List[str]:
    with open(filename, 'r') as file:
        return file.read().splitlines()


class Node:
    def __init__(self, name, parent) -> None:
        self.dirs = {}
        self.files = {}
        self.parent = parent
        self.name = name
        if parent is None:
            self.path = '/'
        elif parent.path == '/':
            self.path = f'/{name}'
        else:
            self.path = f'{parent.path}/{name}'


def parse_all(instructions) -> Node:
    root = Node('/', None)
    current = root
    cd_expr = re.compile(r'\$ cd ([^ ]+)')
    dir_expr = re.compile(r'dir ([^ ]+)')
    file_expr = re.compile(r'(\d+) ([^ ]+)')
    for inst in instructions:
        if cd_expr.match(inst):
            name = cd_expr.findall(inst)[0]
            if name == '..':
                current = current.parent
            elif name == '/':
                current = root
            else:
                current = current.dirs[name]
        elif dir_expr.match(inst):
            name = dir_expr.findall(inst)[0]
            current.dirs[name] = Node(name, current)
        elif file_expr.match(inst):
            (size, name) = file_expr.findall(inst)[0]
            current.files[name] = int(size)
    return root


def print_tree(current: Node, level=0):
    print(f"{'  '*level}- {current.name} (dir), path {current.path}")
    for folder in current.dirs.values():
        print_tree(folder, level+1)
    for (file, size) in current.files.items():
        print(f"{'  '*(level+1)}- {file} (file, size={size}, path)")


def folder_sizes(current: Node) -> Dict[str, int]:
    sizes = {}
    for folder in current.dirs.values():
        sizes.update(folder_sizes(folder))
    files_size = sum(current.files.values())
    subfolders = [c.path for c in current.dirs.values()]
    subfolders_size = sum(size for (path, size)
                          in sizes.items() if path in subfolders)
    sizes[current.path] = files_size + subfolders_size
    return sizes


class Solution(unittest.TestCase):

    def test_star_1(self):
        data = get_input('07-python/input.txt')
        tree = parse_all(data)
        folders = folder_sizes(tree)
        print(sum(size for size in folders.values() if size <= 100000))

    def test_star_2(self):
        data = get_input('07-python/input.txt')
        tree = parse_all(data)
        folders = folder_sizes(tree)
        disk_size = 70000000
        unused_required = 30000000
        unused = disk_size - folders['/']
        to_free = unused_required - unused
        print(min(s for s in folders.values() if s >= to_free))


if __name__ == '__main__':
    unittest.main()
