import random
from enum import IntEnum

import cv2
import numpy as np


EXIT = -1

class Dir(IntEnum):
    UP = 0
    RIGHT = 1
    DOWN = 2
    LEFT = 3


def opposite(direction):
    if direction == Dir.UP:
        return Dir.DOWN
    elif direction == Dir.RIGHT:
        return Dir.LEFT
    elif direction == Dir.DOWN:
        return Dir.UP
    elif direction == Dir.LEFT:
        return Dir.RIGHT


class RectMazeState:
    def __init__(self, num_rows, num_cols):
        self.num_rows, self.num_cols = num_rows, num_cols
        self.reset()

    def reset(self):
        self.tiles = dict()
        self.tiles[EXIT] = set()  # tiles open to boundaries
        for r in range(self.num_rows):
            for c in range(self.num_cols):
                self.tiles[(r, c)] = [None] * 4  # up, right, down, left neighbor idxes
    
    def link(self, idx, direction):
        r, c = idx
        if direction == Dir.UP:
            if r == 0:
                self.tiles[idx][direction] = EXIT
                self.tiles[EXIT].add(idx)
            else:
                self.tiles[idx][direction] = neigh_idx = (r - 1, c)
                self.tiles[neigh_idx][opposite(direction)] = idx
        elif direction == Dir.RIGHT:
            if c == self.num_cols - 1:
                self.tiles[idx][direction] = EXIT
                self.tiles[EXIT].add(idx)
            else:
                self.tiles[idx][direction] = neigh_idx = (r, c + 1)
                self.tiles[neigh_idx][opposite(direction)] = idx
        elif direction == Dir.DOWN:
            if r == self.num_rows - 1:
                self.tiles[idx][direction] = EXIT
                self.tiles[EXIT].add(idx)
            else:
                self.tiles[idx][direction] = neigh_idx = (r + 1, c)
                self.tiles[neigh_idx][opposite(direction)] = idx
        elif direction == Dir.LEFT:
            if c == 0:
                self.tiles[idx][direction] = EXIT
                self.tiles[EXIT].add(idx)
            else:
                self.tiles[idx][direction] = neigh_idx = (r, c - 1)
                self.tiles[neigh_idx][opposite(direction)] = idx


def genMazeBinTree(num_rows, num_cols):
    maze = RectMazeState(num_rows, num_cols)
    c_max = maze.num_cols - 1
    for r in range(maze.num_rows - 1, -1, -1):
        for c in range(maze.num_cols):
            if r == 0 and c == c_max:
                continue
            elif r == 0:
                maze.link((r, c), Dir.RIGHT)
            elif c == num_cols - 1:
                maze.link((r, c), Dir.UP)
            else:
                choose_up = random.randrange(2)
                maze.link((r, c), Dir.UP if choose_up else Dir.RIGHT)
    return maze


def drawMazeAscii(maze):
    for r in range(maze.num_rows):
        for c in range(maze.num_cols):
            print("+   " if maze.tiles[(r, c)][Dir.UP] is not None else "+---", end="")
        print("+")
        for c in range(maze.num_cols):
            print("    " if maze.tiles[(r, c)][Dir.LEFT] is not None else "|   ", end="")
        c = maze.num_cols - 1
        print(" " if maze.tiles[(r, c)][Dir.RIGHT] is not None else "|")
    r = maze.num_rows - 1
    for c in range(maze.num_cols):
        print("+   " if maze.tiles[(r, c)][Dir.DOWN] is not None else "+---", end="")
    print("+")


if __name__ == "__main__":
    maze = genMazeBinTree(5, 5)
    drawMazeAscii(maze)
