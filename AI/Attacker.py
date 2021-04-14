from .BaseAnt import BaseAnt
from .Movement import Explore


class Attacker(BaseAnt):
    def __init__(self, game):
        super(Attacker, self).__init__(game)
        self.movement = Explore(self)
