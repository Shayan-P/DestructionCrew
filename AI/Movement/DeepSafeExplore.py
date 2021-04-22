from AI.Movement import *
from .MovementStrategy import MovementStrategy
from AI.Grid import Grid, Cell


class DeepSafeExplore(MovementStrategy):
    def __init__(self, base_ant):
        super(DeepSafeExplore, self).__init__(base_ant)
        self.previous_purpose = None
        self.reached_destination = False
        # you can remove this

    def get_center_of_unknowns(self):
        if self.previous_purpose is not None:
            if not self.grid.is_unknown(self.previous_purpose):
                self.previous_purpose = None
                self.reached_destination = True
            elif self.grid.unknown_graph.no_path(self.get_now_pos_cell(), self.previous_purpose):
                self.previous_purpose = None
            # and some other condition
        if self.previous_purpose is not None:
            return self.previous_purpose

        opponent_base = self.base_ant.grid.expected_opponent_base()
        candid = None
        for cell in Grid.get_all_cells():
            if self.grid.unknown_graph.no_path(self.get_now_pos_cell(), cell):  # changed to unknown graph
                continue
            if candid is None or opponent_base.manhattan_distance(cell) < opponent_base.manhattan_distance(candid):
                candid = cell
        self.previous_purpose = candid
        return candid

    def get_direction(self):
        print("center of unknowns is ", self.get_center_of_unknowns(), "and my prev turn is ", self.previous_purpose, "there is a path?", self.grid.unknown_graph.no_path(self.get_now_pos_cell(), self.get_center_of_unknowns()))
        return self.go_to(self.get_center_of_unknowns())

    def is_not_good(self):
        if self.previous_purpose is None and self.reached_destination:
            return True
        if self.previous_purpose is not None:
            return not self.grid.is_unknown(self.previous_purpose) or \
                   self.grid.unknown_graph.no_path(self.get_now_pos_cell(), self.previous_purpose)
        return False

    def change_grid_coffs(self):
        self.grid.set_coffs(hate_known=10, opponent_base_fear=5, fight_fear=1, scorpion_fear=1)

    def get_best_path(self, cell_start: Cell, cell_end: Cell):
        if not self.grid.unknown_graph.no_path(cell_start, cell_end):
            return self.grid.unknown_graph.get_shortest_path(cell_start, cell_end)
        return None
