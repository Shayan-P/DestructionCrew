from AI.Movement import *
from .MovementStrategy import MovementStrategy
from Model import CellType, ResourceType
from AI.Grid import Grid, Cell
from AI.BaseAnt import BaseAnt, Config
from AI import Choosing


class GrabAndReturn(MovementStrategy):
    def __init__(self, base_ant):
        super(GrabAndReturn, self).__init__(base_ant)

    def best_strategy(self):
        if self.grid.chat_box_reader.get_now_turn() - self.start_turn > \
                (Config.map_width + Config.map_height) * 0.9:  # need conditions like all cells are known or not ...
            return Explore
        return GrabAndReturn

    def get_direction(self):
        # if you have grabbed it go back to base
        # mage har bar az arzeshesh yeki kam nemishod?
        # if self.game.ant.currentResource.value - self.grid.expected_distance(self.get_now_pos_cell(), self.get_base_cell()) <= 0:
        # change this
        # ino handle konim ke kollan moorche age chizi dasht bere be base
        # todo bebinim moorche ii ke dastesh ja dashte bashe mitoone bazam chi bardare ya na?

        print("We are choosing direction. we have resource: ", self.base_ant.has_resource)
        # shayad bad nabashe ye vaghta tama kone bishtar biare
        # in momkene baes beshe dor khodemoon becharkhim
        if self.base_ant.game.ant.currentResource.value > 0.5 * Config.ant_max_rec_amount:
            return self.go_to_base()
        else:
            return self.go_grab_resource()

    def get_best_cell_score_with_resource(self, current_position: Cell):
        candidates = {}
        for cell in Grid.get_all_cells():
            score = 0
            if self.grid.is_unknown(cell):
                score = 0.5 * self.grid.expected_distance(current_position, cell) + 1  # unknown > emptycell
                # todo injoori ke tamayolesh be raftan jahaye door bishtare!
            elif self.grid.get_cell_resource_type(cell) == ResourceType.GRASS.value:
                score = min(Config.ant_max_rec_amount, self.grid.get_cell_resource_value(cell)) * self.need_grass()
            elif self.grid.get_cell_resource_type(cell) == ResourceType.BREAD.value:
                score = min(Config.ant_max_rec_amount, self.grid.get_cell_resource_value(cell)) * self.need_bread()
            if (not self.grid.is_unknown(cell)) and (self.grid.get_cell_resource_value(cell) is not None) and \
                    (self.grid.get_cell_resource_value(cell) <= 0):
                # todo ask mahdi what is this. get_cell_resource_value is never None
                score = -1000  # -inf
            # age manabe tamoom beshan va hame chiz ro dide bashim ina miterekan
            score -= 0.5 * self.grid.expected_distance(current_position, cell)  # need to change  this
            # ba in taabee momken nist dore khodemoon bekharkhim?
            candidates[cell] = score
        return Choosing.soft_max_choose(candidates)

    def go_grab_resource(self):
        cell = self.get_best_cell_score_with_resource(self.get_now_pos_cell())
        return self.go_to(cell)

    def go_to_base(self):
        print("base cell is ", self.get_base_cell())
        return self.go_to(self.get_base_cell())

    def need_grass(self):
        return 1

    def need_bread(self):
        return 1
