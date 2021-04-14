from .MovementStrategy import MovementStrategy
from Model import CellType, ResourceType
from AI.Grid import Grid, Cell


class GrabAndReturn(MovementStrategy):
    def __init__(self, base_ant):
        super(GrabAndReturn, self).__init__(base_ant)

    def get_direction(self):
        # if you have grabbed it go back to base
        # mage har bar az arzeshesh yeki kam nemishod?
        # if self.game.ant.currentResource.value - self.grid.expected_distance(self.get_now_pos_cell(), self.get_base_cell()) <= 0:
        # change this
        # ino handle konim ke kollan moorche age chizi dasht bere be base
        # todo bebinim moorche ii ke dastesh ja dashte bashe mitoone bazam chi bardare ya na?

        print("We are choosing direction. we have resource: ", self.base_ant.has_resource)
        if self.base_ant.has_resource:
            return self.go_to_base()
        else:
            return self.go_grab_resource()

    def get_best_cell_score_with_resource(self, current_position: Cell):
        # score must be expected value
        best_cell = None
        best_score = -1

        # todo
        # change this
        for cell in Grid.get_all_cells():
            score = 0
            # dar yek khoone momkene do no manbaa bashan?
            if self.grid.is_unknown(cell):
                score = 0
            elif self.grid.get_cell_resource_type(cell) == ResourceType.GRASS.value:
                score = min(10, self.grid.get_cell_resource_value(cell)) * 0.5  # in 10 avaz she
            elif self.grid.get_cell_resource_type(cell) == ResourceType.BREAD.value:
                score = min(10, self.grid.get_cell_resource_value(cell))  # in 10 avaz she
            if (not self.grid.is_unknown(cell)) and (self.grid.get_cell_resource_value(cell) is not None) and \
                    (self.grid.get_cell_resource_value(cell) <= 0):
                # don't try to go to seen cells. also change this.
                score = -1000  # inf
            # age manabe tamoom beshan va hame chiz ro dide bashim ina miterekan
            score -= 0.5 * self.grid.expected_distance(current_position, cell)  # need to change  this
            # ba in taabee momken nist dore khodemoon bekharkhim?
            if best_cell is None or best_score < score:
                best_cell = cell
                best_score = score
        return best_cell, best_score

    def go_grab_resource(self):
        cell, score = self.get_best_cell_score_with_resource(self.get_now_pos_cell())
        return self.go_to(cell)

    def go_to_base(self):
        print("base cell is ", self.get_base_cell())
        return self.go_to(self.get_base_cell())


