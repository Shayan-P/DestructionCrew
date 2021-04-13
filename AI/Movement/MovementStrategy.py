from AI.Grid import Grid
from AI.BaseAnt import BaseAnt
from AI.Cell import Cell


class MovementStrategy:
    def __init__(self, base_ant: BaseAnt):
        self.base_ant: BaseAnt = base_ant
        self.grid: Grid = base_ant.grid
        self.get_now_pos_cell: Cell = base_ant.get_now_pos_cell
        self.get_base_cell: Cell = base_ant.get_base_cell
        # is this ok?

    def get_direction(self):
        NotImplementedError

    def go_to(self, destination: Cell):
        path = self.grid.get_best_path(self.get_now_pos_cell(), destination)
        # what if path is None?
        print("going to ", destination, "path is ", *path)
        return self.get_first_step_direction(path)

    def get_first_step_direction(self, path):
        assert path[0] == self.get_now_pos_cell()
        assert len(path) > 1

        # this is tof
        if self.grid.get_cell_resource_value(path[1]) > 0:
            self.base_ant.has_resource = True
            # hatman hatman hatman change this

        return path[0].direction_to(path[1])
