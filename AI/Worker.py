from .BaseAnt import BaseAnt
from .Movement import GrabAndReturn, Explore


class Worker(BaseAnt):
    def __init__(self, game):
        super(Worker, self).__init__(game)
        self.movement = GrabAndReturn(self)

    def get_move(self):
        self.pre_move()
        self.choose_best_strategy()
        return self.movement.get_direction()

    def choose_best_strategy(self):
        best_strategy = self.movement.best_strategy()
        del self.movement
        self.movement = best_strategy(self)
