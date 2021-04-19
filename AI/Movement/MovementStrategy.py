from AI.Grid import Grid
from AI.BaseAnt import BaseAnt
from AI.Grid.Cell import Cell
from AI.Config import Config


class MovementStrategy:
    def __init__(self, base_ant: BaseAnt):
        self.base_ant: BaseAnt = base_ant
        self.grid: Grid = base_ant.grid

    def get_now_pos_cell(self):
        return Cell(Config.now_x, Config.now_y)

    def get_base_cell(self):
        return Cell(Config.base_x, Config.base_y)

    def get_direction(self):
        NotImplementedError

    def get_best_path(self, cell_start: Cell, cell_end: Cell):
        # nabayad chizaii ke midim be graph mutable bashe? age avazesh kone chi?
        if not self.grid.known_graph.no_path(cell_start, cell_end):
            return self.grid.known_graph.get_shortest_path(cell_start, cell_end)
        # if not self.unknown_graph.no_path(cell_start, cell_end):
        #    return self.unknown_graph.get_shortest_path(cell_start, cell_end)
        return None

    def go_to(self, destination: Cell):
        path = self.get_best_path(self.get_now_pos_cell(), destination)
        # print("now we are in ", self.get_now_pos_cell(), "we want to go to ", destination, "path is", path)
        # what if path is None?
        print("going to ", destination, "path is ", *path)
        return self.get_first_step_direction(path)

    def get_first_step_direction(self, path):
        assert path[0] == self.get_now_pos_cell()
        if len(path) == 1:
            # print("alert! size of path is 1")
            return path[0].direction_to(path[0])
        return path[0].direction_to(path[1])
