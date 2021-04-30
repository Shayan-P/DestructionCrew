import random

from .BaseAnt import BaseAnt
from .Movement import GrabAndReturn, Explore, Follower, DeepSafeExplore, AloneSpy
from AI.Config import Config


class Worker(BaseAnt):
    def __init__(self, game):
        super(Worker, self).__init__(game)
        self.spy = False

    def get_move(self):
        ret = super(Worker, self).get_move()
        return self.escape_from_great_danger_filter(ret)

    def choose_best_strategy(self):
        # if there are a little unknown cells stop exploring todo
        if self.previous_strategy is None:
            self.previous_strategy = Explore
            self.previous_strategy_object = Explore(self)
        if self.game.ant.currentResource.value >= Config.ant_max_rec_amount * 0.5:
            self.spy = False
            return GrabAndReturn
        grab_and_return_object = self.previous_strategy_object if self.previous_strategy is GrabAndReturn else GrabAndReturn(self)
        if grab_and_return_object.is_really_good():
            self.spy = False
            return GrabAndReturn

        if self.grid.chat_box_reader.get_now_turn() >= 30 and Config.alive_turn == 0 and random.random() <= 0.3:
            self.spy = True
            if random.random() <= 0.5:
                print("sending deep safe explorer")
                return DeepSafeExplore
            else:
                print("sending alone spy")
                return AloneSpy
        if self.spy:
            return self.previous_strategy

        if self.previous_strategy is GrabAndReturn:
            self.spy = False
            return Explore
        return self.previous_strategy
