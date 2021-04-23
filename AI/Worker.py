import random

from .BaseAnt import BaseAnt
from .Movement import GrabAndReturn, Explore, Follower, DeepSafeExplore, AloneSpy
from AI.Config import Config


class Worker(BaseAnt):
    def __init__(self, game):
        super(Worker, self).__init__(game)
        self.movement = GrabAndReturn(self)

    def choose_best_strategy(self):
        if self.previous_strategy is None:
            self.previous_strategy = GrabAndReturn
            self.previous_strategy_object = GrabAndReturn(self)
        if self.game.ant.currentResource.value > Config.ant_max_rec_amount * 0.5:
            return GrabAndReturn
        # momkene ye chiz kam dastet bashe baad be khatere oon natooni chizi bardari. todo fix this
        if GrabAndReturn(self).is_really_good():
            return GrabAndReturn

        if self.previous_strategy is GrabAndReturn:
            rnd = random.random()
            if rnd <= 0.3:
                return AloneSpy
            if rnd <= 0.5:
                return DeepSafeExplore
            return Explore
        return self.previous_strategy
