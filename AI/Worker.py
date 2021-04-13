from .BaseAnt import BaseAnt
from .Movement import GrabAndReturn, Explore


class Worker(BaseAnt):
    def __init__(self, game):
        super(Worker, self).__init__(game)
        self.movement = GrabAndReturn(self)

    def get_move(self):
        self.pre_move()
        return self.movement.get_direction()
