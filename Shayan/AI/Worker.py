from .Map import *
import random


class Worker:
    def __init__(self, game):
        self.game = game
        self.grid = Grid(game)
        self.dfs_generator = self.dfs(self.get_now_pos())

    def get_message(self):
        return "man worker am", 10

    def get_move(self):
        view_distance = self.game.viewDistance
        print("VIEW IS ", view_distance)
        if view_distance == 0:  # ina bug zadan ino 0 midan!
            view_distance = 8
        for dx in range(-view_distance-2, view_distance+2):
            for dy in range(-view_distance-2, view_distance+2):
                cell = self.game.ant.getMapRelativeCell(dx, dy)
                if cell is not None:
                    self.grid.see_cell(cell)

        print("I'm in", self.get_now_pos())
        self.grid.print_all_we_know_from_map()

        x = next(self.dfs_generator)
        print("I moved", x)
        return x.value

    def get_now_pos(self):
        return Cell(self.game.ant.currentX, self.game.ant.currentY)

    def dfs(self, now):
        self.grid.visit_cell(now)
        my_directions = DIRECTIONS.copy()
        random.shuffle(my_directions)
        for direction in my_directions:
            nxt = now.go_to(direction)
            if not self.grid.is_visited(nxt) and not self.grid.is_wall(nxt):
                yield direction
                yield from self.dfs(nxt)
                yield nxt.direction_to(now)
