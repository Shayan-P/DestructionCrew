import random

import Model
from AI.Movement import *
from .MovementStrategy import MovementStrategy
from AI.Grid import Grid, Cell
from AI.Grid.Cell import get_random_directions
from AI.Choosing import soft_max_choose
from AI.Config import Config


class Explore(MovementStrategy):
    def __init__(self, base_ant):
        super(Explore, self).__init__(base_ant)
        self.previous_purpose = None

    def get_one_of_near_unknowns(self):
        candidates = {}
        current_position = self.base_ant.get_now_pos_cell()
        if self.previous_purpose is not None and not self.grid.is_unknown(self.previous_purpose):
            self.previous_purpose = None
        if self.previous_purpose is not None:
            candidates[self.previous_purpose] = 3  # change this todo
        for cell in Grid.get_all_cells():
            if self.grid.is_unknown(cell) and not self.grid.known_graph.no_path(self.base_ant.get_now_pos_cell(), cell):
                distance = self.grid.expected_distance(current_position, cell)
                if cell not in candidates:
                    candidates[cell] = 0
                candidates[cell] += -distance
                for dx in range(-3, 4):
                    for dy in range(-3, 4):
                        if self.grid.base_trap_graph.no_path(self.get_base_cell(), cell.move_to(dx, dy)):
                            continue
                        if self.grid.get_cell_resource_value(cell.move_to(dx, dy)) > 0:
                            candidates[cell] += (5 - abs(dx) + abs(dy)) * 0.3  # change this todo
        if len(candidates) == 0:
            return None
        self.previous_purpose = soft_max_choose(candidates)
        return self.previous_purpose

    def get_direction(self):
        # fix this every where todo
        X = self.get_one_of_near_unknowns()
        if X is None:
            return random.choice(get_random_directions())
        return self.go_to(self.get_one_of_near_unknowns())
