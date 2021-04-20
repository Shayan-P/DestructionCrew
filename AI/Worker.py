import random

from .BaseAnt import BaseAnt
from .Movement import GrabAndReturn, Explore, Follower, FuckOpponentBase
from AI.Config import Config


class Worker(BaseAnt):
    def __init__(self, game):
        super(Worker, self).__init__(game)
        self.movement = GrabAndReturn(self)

    def choose_best_strategy(self):
        if self.grid.chat_box_reader.get_now_turn() >= 30 and self.game.alive_turn <= 3 and random.random() <= 0.15:
            return FuckOpponentBase  # go get fucked and save the team!
        if self.previous_strategy is FuckOpponentBase:
            return FuckOpponentBase
        # change this todo

        # if there are a little unknown cells stop exploring todo
        if self.previous_strategy is None:
            self.previous_strategy = GrabAndReturn
            self.previous_strategy_object = GrabAndReturn(self)
        if self.game.ant.currentResource.value > Config.ant_max_rec_amount * 0.5:
            return GrabAndReturn
        # momkene ye chiz kam dastet bashe baad be khatere oon natooni chizi bardari. todo fix this
        if (self.previous_strategy is not GrabAndReturn) and GrabAndReturn(self).is_really_good():
            return GrabAndReturn
        if self.previous_strategy is GrabAndReturn and self.previous_strategy_object.is_not_good():
            return Explore
        if self.previous_strategy is Explore:
            return Explore
        return GrabAndReturn
