from .BaseAnt import BaseAnt
from .Movement import GrabAndReturn
from Model import Direction

class Worker(BaseAnt):
    def __init__(self, game):
        super(Worker, self).__init__(game)
        self.movement = GrabAndReturn(self)

    def get_move(self):
        self.pre_move()
        return Direction.UP
#        return self.movement.get_direction()
