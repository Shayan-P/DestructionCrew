import Model

from .BaseAnt import BaseAnt
from .Grid import Cell, Grid
from .Movement import Explore, Follower, AloneSpy, Defender, GrabAndReturn, GoCamp, FuckOpponentBase, GetNearOpponentBase
from .ChatBox import Gathering
from random import randint, random
from AI.Config import Config
from typing import Optional

class Attacker(BaseAnt):
    def __init__(self, game):
        super(Attacker, self).__init__(game)
        self.movement = Defender(self)

    def spread_filter(self, move):
        us = len(self.near_scorpions(0))
        if us == 1:
            return move
        if random() < 0.25:
            return Model.Direction.CENTER
        return move

    def get_move(self):
        ret = super(Attacker, self).get_move()
        if self.previous_strategy is FuckOpponentBase:
            return ret
        elif self.previous_strategy is Explore:
            return self.escape_from_great_danger_filter(ret)
        elif self.previous_strategy is GoCamp:
            return ret
        return ret

    def near_scorpions(self, distance):
        return list(filter(
             lambda e: e.antTeam == Model.AntTeam.ALLIED.value and e.antType == Model.AntType.SARBAAZ.value,
             self.grid.get_near_cell_ants(cell=self.get_now_pos_cell(), distance=distance)
        ))

    def choose_best_strategy(self):
        # if not self.grid.sure_opponent_base():
        #     if self.previous_strategy is AloneSpy:
        #         return AloneSpy
        #     if Config.alive_turn == 1 and random() < 0.06:
        #         return AloneSpy

        # if self.previous_strategy is GetNearOpponentBase:
        #     return GetNearOpponentBase
        # if (self.previous_strategy is FuckOpponentBase) and (self.grid.sure_opponent_base()) and (len(self.near_scorpions(2)) >= 3):
        #     return GetNearOpponentBase

        if self.grid.sure_opponent_base() and self.get_now_pos_cell().manhattan_distance(self.grid.expected_opponent_base()) <= Config.base_range:
            return FuckOpponentBase
        if self.grid.chat_box_reader.get_now_turn() >= 100: # change this if. to something like if map is partially known... todo
            if len(self.near_scorpions(1)) >= 7: # change this todo
                return FuckOpponentBase
        if self.previous_strategy is FuckOpponentBase:
            return FuckOpponentBase
        if self.grid.chat_box_reader.get_now_turn() >= 165:  # change this! todo
            return FuckOpponentBase
        if self.grid.chat_box_reader.get_now_turn() >= 150 and self.grid.sure_opponent_base():
            return FuckOpponentBase
        # if there are a little unknown cells stop exploring todo
        # return GoCamp
        if self.previous_strategy is None:
            if GoCamp(self).is_not_good():
                self.previous_strategy = Explore
            else:
                self.previous_strategy = GoCamp
            self.previous_strategy_object = self.previous_strategy(self)

        # # momkene ye chiz kam dastet bashe baad be khatere oon natooni chizi bardari. todo fix this
        if self.previous_strategy is GoCamp:
            return GoCamp
        if GoCamp(self).is_not_good():
            return Explore
        # if self.previous_strategy is Explore:
        #     return Explore
        return GoCamp
