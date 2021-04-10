from .BaseAnt import BaseAnt
from .Movement import Explore
from Model import Direction


class Attacker(BaseAnt):
    def __init__(self, game):
        super(Attacker, self).__init__(game)
        self.movement = Explore(self)

    def get_move(self):
        self.pre_move()
        return Direction.DOWN
#        return self.movement.get_direction()

