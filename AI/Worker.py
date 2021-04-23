import random

from .BaseAnt import BaseAnt
from .Movement import GrabAndReturn, Explore, Follower, DeepSafeExplore, AloneSpy
from AI.Config import Config


class Worker(BaseAnt):
    def __init__(self, game):
        super(Worker, self).__init__(game)
        self.movement = GrabAndReturn(self)
        self.spy = False

    def choose_best_strategy(self):
        return DeepSafeExplore
        # if there are a little unknown cells stop exploring todo
        if self.grid.chat_box_reader.get_now_turn() >= 35 and self.game.alive_turn == 0 and random.random() <= 0.3:
            self.spy = True
        if self.spy:
            return AloneSpy

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
