import Model

from .BaseAnt import BaseAnt
from .Movement import Explore, Follower, Defender, GrabAndReturn, GoCamp, FuckOpponentBase
from random import randint
from AI.Config import Config


class Attacker(BaseAnt):
    def __init__(self, game):
        super(Attacker, self).__init__(game)
        self.movement = Defender(self)
        self.stays_in_group = None

    def get_move(self):
        ret = super(Attacker, self).get_move()

        us = len(self.near_scorpions(0))
        for dx in range(-1, 2):
            for dy in range(-1, 2):
                if abs(dx) + abs(dy) == 1:
                    adj_cell = self.get_now_pos_cell().move_to(dx, dy)
                    cnt = 0
                    for ant in self.grid.get_near_cell_ants(adj_cell, 0):
                        if (ant.antTeam == Model.AntTeam.ALLIED.value) and (ant.antType == Model.AntType.SARBAAZ.value):
                            cnt += 1
                    if (cnt > us) or ((cnt == us) and (min(dx, dy) == -1) ):
                        return self.get_now_pos_cell().direction_to(adj_cell)
        return ret
        # also you have to remove this part in order to remove stay_in_group
        #
        # if not self.stays_in_group:
        #     return ret
        # near_scorpions = len(list(filter(
        #     lambda e: e.antTeam == Model.AntTeam.ALLIED.value and e.antType == Model.AntType.SARBAAZ.value,
        #     self.grid.get_near_cell_ants(cell=self.get_now_pos_cell(), distance=2)
        # )))
        # if near_scorpions < 3:
        #     return Model.Direction.CENTER
        # return ret

    def near_scorpions(self, distance):
        return list(filter(
             lambda e: e.antTeam == Model.AntTeam.ALLIED.value and e.antType == Model.AntType.SARBAAZ.value,
             self.grid.get_near_cell_ants(cell=self.get_now_pos_cell(), distance=distance)
        ))

    def choose_best_strategy(self):
        # this will probably cause some bugs!
        if self.stays_in_group is None:
            if self.grid.chat_box_reader.get_now_turn() <= 10:
                self.stays_in_group = False
            elif randint(1, 10) <= 6:
                self.stays_in_group = True
            else:
                self.stays_in_group = False

        if self.grid.chat_box_reader.get_now_turn() >= 63: # change this if. to something like if map is partially known... todo
            if len(self.near_scorpions(2)) >= 7: # change this todo
                return FuckOpponentBase
        if self.previous_strategy is FuckOpponentBase:
            return FuckOpponentBase
        if self.grid.chat_box_reader.get_now_turn() >= 82:  # change this! todo
            return FuckOpponentBase

        # if there are a little unknown cells stop exploring todo
        # return GoCamp
        if self.previous_strategy is None:
            self.previous_strategy = Explore
            self.previous_strategy_object = Explore(self)
        # if self.game.ant.currentResource.value > Config.ant_max_rec_amount * 0.5:
        #     return GoCamp
        # # momkene ye chiz kam dastet bashe baad be khatere oon natooni chizi bardari. todo fix this
        # if (self.previous_strategy is not GoCamp) and GoCamp(self).is_really_good():
        #     return GoCamp
        if self.previous_strategy is GoCamp:
            return GoCamp
        if GoCamp(self).is_not_good():
            return Explore
        # if self.previous_strategy is Explore:
        #     return Explore
        return GoCamp
