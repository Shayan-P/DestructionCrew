from ..Movement import *
from AI.Grid import Grid, Cell
from AI.Choosing import soft_max_choose
import Config

class Explore(MovementStrategy):
    def __init__(self, base_ant):
        super(Explore, self).__init__(base_ant)

    def best_strategy(self):
        if self.base_ant.currentResource.value > 0.5 * Config.ant_max_rec_amount:
            return GrabAndReturn
        return Explore

    def get_one_of_near_unknowns(self, current_position: Cell):
        candidates = {}
        for cell in Grid.get_all_cells():
            if self.grid.is_unknown(cell):
                distance = self.grid.expected_distance(current_position, cell)
                candidates[cell] = -distance
                # age yeki az 1000 ha bardashte beshe badbakht mishim
                if distance != 1000:
                    print("can go to ", cell, "distance is ", distance)
        return soft_max_choose(candidates)

    def get_direction(self):
        # this has some bugs.
        # you must not change your destination after you fixed it!
        return self.go_to(self.get_one_of_near_unknowns(self.get_now_pos_cell()))
