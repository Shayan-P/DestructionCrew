from AI.Grid import Grid
from AI.BaseAnt import BaseAnt
from AI.Grid.Cell import Cell
from AI.Config import Config


class MovementStrategy:
    def __init__(self, base_ant: BaseAnt):
        self.base_ant: BaseAnt = base_ant
        self.grid: Grid = base_ant.grid
        self.change_grid_coffs()

    def get_now_pos_cell(self):
        return Cell(Config.now_x, Config.now_y)

    def get_base_cell(self):
        return Cell(Config.base_x, Config.base_y)

    def get_direction(self):
        NotImplementedError

    def go_to(self, destination: Cell, graph=None):
        if graph is None:
            graph = self.grid.known_graph
        if not graph.no_path(self.get_now_pos_cell(), destination):
            path = graph.get_shortest_path(self.get_now_pos_cell(), destination)
            return self.get_first_step_direction(path)

    def get_first_step_direction(self, path):
        assert path[0] == self.get_now_pos_cell()
        if len(path) == 1:
            # print("alert! size of path is 1")
            return path[0].direction_to(path[0])
        return path[0].direction_to(path[1])

    def change_grid_coffs(self):
        self.grid.set_coffs(hate_known=0, opponent_base_fear=1)
