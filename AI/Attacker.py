from .BaseAnt import BaseAnt
from .Movement import Explore


class Attacker(BaseAnt):
    def __init__(self, game):
        super(Attacker, self).__init__(game)
        self.movement = Explore(self)

    def get_move(self):
        super(Attacker, self).get_move()
        return self.movement.get_direction()

