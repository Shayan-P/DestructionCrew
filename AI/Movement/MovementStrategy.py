from AI.Grid import Grid
from AI.BaseAnt import BaseAnt
from AI.Grid.Cell import Cell


class MovementStrategy:
    def __init__(self, base_ant: BaseAnt):
        # dont save base_ant
        self.grid: Grid = base_ant.grid
        self.get_now_pos_cell = base_ant.get_now_pos_cell
        self.get_base_cell = base_ant.get_base_cell
        # is this ok?

    def get_direction(self):
        NotImplementedError

    def get_best_path(self, cell_start: Cell, cell_end: Cell):
        # nabayad chizaii ke midim be graph mutable bashe? age avazesh kone chi?
        print(self.grid.known_graph.no_path(cell_start, cell_end), self.grid.known_graph.get_shortest_path(cell_start, cell_end))
        if not self.grid.known_graph.no_path(cell_start, cell_end):
            return self.grid.known_graph.get_shortest_path(cell_start, cell_end)
        # if not self.unknown_graph.no_path(cell_start, cell_end):
        #    return self.unknown_graph.get_shortest_path(cell_start, cell_end)
        return None

    def go_to(self, destination: Cell):
        path = self.get_best_path(self.get_now_pos_cell(), destination)
        print("now we are in ", self.get_now_pos_cell(), "we want to go to ", destination, "path is", path)
        # what if path is None?
        print("going to ", destination, "path is ", *path)
        return self.get_first_step_direction(path)

    def get_first_step_direction(self, path):
        assert path[0] == self.get_now_pos_cell()
        assert len(path) > 1
        return path[0].direction_to(path[1])
