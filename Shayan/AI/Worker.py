from .Map import *
from Model import Direction
import random


class Worker:
    def __init__(self, game):
        self.game = game
        self.grid = Grid(game.mapWidth, game.mapHeight)
        self.dfs_generator = self.dfs(self.get_now_pos())

    def get_message(self):
        return "man worker am", 10

    def get_move(self):
        x = next(self.dfs_generator)
        print("I moved", x)
        return x.value

    def get_now_pos(self):
        return Cell(self.game.ant.currentX, self.game.ant.currentY)

    def dfs(self, now):
        self.grid.put_cell(now, 0)
        directions = [Direction.UP, Direction.DOWN, Direction.LEFT, Direction.RIGHT]
        random.shuffle(directions)
        for direction in directions:
            nxt = now.adjacent(direction)
            if self.grid.is_unknown(nxt) and self.game.ant.getMapRelativeCell(nxt.x-now.x, nxt.y-now.y) == CellType.EMPTY:
                yield direction
                self.grid.put_cell(nxt, 0)
                if nxt != self.get_now_pos():
                    continue
                yield from self.dfs(nxt)
                yield nxt.direction_to(now)
