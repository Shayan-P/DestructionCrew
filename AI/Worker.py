import random

from .BaseAnt import BaseAnt
from .Movement import GrabAndReturn, Explore, Follower, DeepSafeExplore
from AI.Config import Config


class Worker(BaseAnt):
    def __init__(self, game):
        super(Worker, self).__init__(game)
        self.movement = GrabAndReturn(self)
        self.spy = False

    def choose_best_strategy(self):
        # if there are a little unknown cells stop exploring todo
        if self.grid.chat_box_reader.get_now_turn() >= 35 and self.game.alive_turn == 0 and random.random() <= 0.15:
            self.spy = True
        if self.spy and self.previous_strategy is not None and self.previous_strategy_object.is_not_good():
            self.spy = False
        if self.spy:
            return DeepSafeExplore

        if self.previous_strategy is None:
            self.previous_strategy = GrabAndReturn
            self.previous_strategy_object = GrabAndReturn(self)
        if self.game.ant.currentResource.value > Config.ant_max_rec_amount * 0.5:
            return GrabAndReturn
        # momkene ye chiz kam dastet bashe baad be khatere oon natooni chizi bardari. todo fix this
        if GrabAndReturn(self).is_really_good():
            return GrabAndReturn

        if self.previous_strategy is DeepSafeExplore and not self.previous_strategy_object.is_not_good():
            return DeepSafeExplore

        if self.previous_strategy is GrabAndReturn and self.previous_strategy_object.is_not_good():
            return DeepSafeExplore
        if self.previous_strategy is DeepSafeExplore:
            return DeepSafeExplore
        return GrabAndReturn
