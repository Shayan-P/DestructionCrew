from .BaseAnt import BaseAnt
from .Movement import Explore, Follower


class Attacker(BaseAnt):
    def __init__(self, game):
        super(Attacker, self).__init__(game)
        self.movement = Explore(self)

    def get_move(self):
        self.pre_move()
        self.choose_best_strategy()
        return self.movement.get_direction()

    def choose_best_strategy(self):
        best_strategy = self.movement.best_strategy()
        del self.movement
        self.movement = best_strategy(self)
