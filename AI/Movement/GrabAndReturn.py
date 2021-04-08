from .MovementStrategy import MovementStrategy


class GrabAndReturn(MovementStrategy):
    def __init__(self, base_ant):
        super(GrabAndReturn, self).__init__(base_ant)

    def get_direction(self):
        # if you have grabbed it go back to base
        # mage har bar az arzeshesh yeki kam nemishod?
        # if self.game.ant.currentResource.value - self.grid.expected_distance(self.get_now_pos_cell(), self.get_base_cell()) <= 0:
        # change this
        print("We are choosing direction. we have resource: ", self.base_ant.has_resource)
        if self.base_ant.has_resource:
            return self.go_to_base()
        else:
            return self.go_grab_resource()

    def go_grab_resource(self):
        cell, score = self.grid.get_best_cell_score_with_resource(self.get_now_pos_cell())
        return self.go_to(cell)

    def go_to_base(self):
        return self.go_to(self.get_base_cell())


