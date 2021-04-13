from .BaseAnt import BaseAnt
from .Movement import Explore, Follower


class Attacker(BaseAnt):
    def __init__(self, game):
        super(Attacker, self).__init__(game)
        self.movement = Follower(self)

    def get_move(self):
        self.pre_move()
        return self.movement.get_direction()

