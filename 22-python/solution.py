from __future__ import annotations
import unittest
from typing import List
import re


def get_input(filename: str) -> List[int]:
    with open(filename, 'r') as file:
        lines = file.read().splitlines()
        grid, rules = lines[:-2], lines[-1]
        split_rules = [s if s in 'RL' else int(s) for s in re.findall(r"([RL]|\d+)", rules)]
        width = max([len(line) for line in grid])
        grid = [" " + line.ljust(width) + " " for line in grid]
        width += 2
        grid = [" "*width] + grid + [" "*width]
        return grid, split_rules

OFFSETS = [(0, 1), (1, 0), (0, -1), (-1, 0)]


def get_next(direction, y, x, row_start, row_end, col_start, col_end):
    if direction == 0 and x+1 >= row_end[y]:
        return direction, y, row_start[y]
    elif direction == 1 and y+1 >= col_end[x]:
        return direction, col_start[x], x
    elif direction == 2 and x-1 < row_start[y]:
        return direction, y, row_end[y]-1
    elif direction == 3 and y-1 < col_start[x]:
        return direction, col_end[x]-1, x
    dy,dx = OFFSETS[direction]
    return direction, y+dy, x+dx


def part1(grid, rules):
    row_start = [next((idx_char for idx_char, char in enumerate(row) if char in '.#'), 0) for row in grid]
    row_end = [next((len(row)-idx_char for idx_char, char in enumerate(row[::-1]) if char in '.#'), 0) for row in grid]
    col_start = [next((idx_char for idx_char, char in enumerate(row) if char in '.#'), 0) for row in zip(*grid)]
    col_end = [next((len(row)-idx_char for idx_char, char in enumerate(row[::-1]) if char in '.#'), 0) for row in zip(*grid)]
    direction, (y, x) = 0, (1, row_start[1])
    for rule in rules:
        if isinstance(rule, str):
            direction = (direction + (-1 if rule == 'L' else 1)) % 4
        else:
            for _ in range(rule):
                direction, next_y, next_x = get_next(direction, y, x, row_start, row_end, col_start, col_end)
                if grid[next_y][next_x] == '#':
                    break
                y, x = (next_y, next_x)
    return 1000*y+4*x+direction

def part2(grid, ins_list):
    width = len(grid[0])-2
    height = len(grid)-2
    dir, (x, y) = 0, (1, 1)
    for j in range(width):
        if grid[1][j] == ".":
            y=j
            break
    dir_cache = (x,y)
    face_size = round(pow(sum([c != " " for line in grid for c in line])//6,0.5))
    Q = [dir_cache]
    visited = {dir_cache:[None]*4}
    while len(Q) > 0:
        v, *Q = Q
        x,y=v
        for dir in range(4):
            i,j = OFFSETS[dir]
            i,j = x+i*face_size,y+j*face_size
            if not(0 <= i < height and 0 <= j < width):
                continue
            if grid[i][j] == " ":
                continue
            w = (i,j)
            if w not in visited:
                visited[v][dir] = w
                w_list = [None]*4
                w_list[(dir+2)%4] = v
                visited[w] = w_list
                Q += [w]
    faces = {}
    for (i,j),_ in visited.items():
        faces[(i//face_size,j//face_size)] = [((v[0]//face_size,v[1]//face_size) if v is not None else v) for v in visited[(i,j)]]
    while sum([edge is None for key in faces for edge in faces[key]]) > 0:
        for face,_ in faces.items():
            for dir in range(4):
                if faces[face][dir] is None:
                    for delta in -1,1:
                        common_face = faces[face][(dir+delta)%4]
                        if common_face is None:
                            continue
                        common_face_edge = faces[common_face].index(face)
                        missing_face = faces[common_face][(common_face_edge+delta)%4]
                        if missing_face is None:
                            continue
                        missing_face_edge = faces[missing_face].index(common_face)
                        faces[missing_face][(missing_face_edge+delta)%4] = face
                        faces[face][dir] = missing_face
                        break
    x,y = dir_cache
    dir = 0
    edge_top_offset_out = [[1,1],[1,face_size],[face_size,face_size],[face_size,1]]
    for step in ins_list:
        if step == "R":
            dir = (dir+1)%4
        elif step == "L":
            dir = (dir-1)%4
        else:
            dx,dy = OFFSETS[dir]
            new_dir = dir
            for i in range(step):
                nx,ny = x+dx,y+dy
                if grid[nx][ny] == " ":
                    cur_face = (x-1)//face_size,(y-1)//face_size
                    cur_offset = 0
                    while tuple([a*face_size+b+c*cur_offset for a,b,c in zip(cur_face,edge_top_offset_out[(dir+1)%4],OFFSETS[(dir+1)%4])]) != (x,y):
                        cur_offset += 1
                    next_face = faces[cur_face][dir]
                    new_dir = (faces[next_face].index(cur_face) + 2) % 4
                    nx,ny = tuple([a*face_size+b+c*cur_offset for a,b,c in zip(next_face,edge_top_offset_out[new_dir],OFFSETS[(new_dir+1)%4])])
                if grid[nx][ny] == "#":
                    break
                else:
                    x,y = nx,ny
                    dir = new_dir
                    dx,dy = OFFSETS[dir]
    return x*1000+y*4+dir

class Solution(unittest.TestCase):

    def test_star_1(self):
        grid, rules = get_input('22-python/input.txt')
        print(part1(grid, rules))

    def test_star_2(self):
        grid, rules = get_input('22-python/input.txt')
        print(part2(grid, rules))


if __name__ == '__main__':
    unittest.main()
