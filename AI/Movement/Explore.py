from AI.Movement import *
from .MovementStrategy import MovementStrategy
from AI.Grid import Grid, Cell
from AI.Choosing import soft_max_choose
from AI.Config import Config


class Explore(MovementStrategy):
    def __init__(self, base_ant):
        super(Explore, self).__init__(base_ant)

    def best_strategy(self):
        # todo ye if ham bezarim ke kheili az mabda door nashe.
        # age ye manbaadashte bashe mitoone az yek nooe dige ham bardare?
        if self.base_ant.game.ant.currentResource.value > 0.5 * Config.ant_max_rec_amount:
            return GrabAndReturn
        # todo change this if.
        # if there is a resource near me. go grab it.
        # if there is no near resource then go explore!
        if self.grid.chat_box_reader.get_now_turn() > Config.max_turn * 0.8:
            return GrabAndReturn
        return Explore

    def get_one_of_near_unknowns(self, current_position: Cell):
        candidates = {}
        for cell in Grid.get_all_cells():
            if self.grid.is_unknown(cell):
                distance = self.grid.expected_distance(current_position, cell)
                candidates[cell] = -distance
                # age yeki az 1000 ha bardashte beshe badbakht mishim
                # todo : motmaen shim ke 1000 ha ro bar nemidarim. magar na runtime error mikhorim.
            elif self.grid.get_cell_resource_value(cell) > 0:
                distance = self.grid.expected_distance(current_position, cell)
                candidates[cell] = -(distance ** 1.5)  # can be optimized
        return soft_max_choose(candidates)

    def get_direction(self):
        # this has some bugs.
        # you must not change your destination after you fixed it!
        # dor khodesh micharkhe!
        return self.go_to(self.get_one_of_near_unknowns(self.get_now_pos_cell()))
