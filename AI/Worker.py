from .BaseAnt import BaseAnt
from .Movement import GrabAndReturn, Explore, Follower
from AI.Config import Config


class Worker(BaseAnt):
    def __init__(self, game):
        super(Worker, self).__init__(game)
        self.movement = GrabAndReturn(self)

    def choose_best_strategy(self):
        # if there are a little unknown cells stop exploring todo
        if self.previous_strategy is None:
            self.previous_strategy = GrabAndReturn
            self.previous_strategy_object = GrabAndReturn(self)
        if self.game.ant.currentResource.value > Config.ant_max_rec_amount * 0.5:
            return GrabAndReturn
        if self.previous_strategy is GrabAndReturn and self.previous_strategy_object.not_good():
            return Explore
        if self.previous_strategy is Explore:
            return Explore
        return GrabAndReturn
