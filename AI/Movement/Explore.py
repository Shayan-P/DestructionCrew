from .MovementStrategy import MovementStrategy


class Explore(MovementStrategy):
    def __init__(self, base_ant):
        super(Explore, self).__init__(base_ant)

    def get_direction(self):
        # this has some bugs.
        # you must not change your destination after you fixed it!
        return self.go_to(self.grid.get_one_of_near_unknowns(self.get_now_pos_cell()))
