import Model

from .BaseAnt import BaseAnt
from .Movement import Explore, Follower, Defender, GrabAndReturn, GoCamp
from random import randint
from AI.Config import Config


class Attacker(BaseAnt):
    def __init__(self, game):
        super(Attacker, self).__init__(game)
        self.movement = Defender(self)
        self.stays_in_group = None

    def get_move(self):
        ret = super(Attacker, self).get_move()
        if not self.stays_in_group:
            return ret
        near_scorpions = 0
        for dx in range(-2, 3):
            for dy in range(-2, 3):
                cell = self.get_now_pos_cell().move_to(dx, dy)
                for ant in self.grid.get_cell_ants(cell):
                    if ant.antTeam == Model.AntTeam.ALLIED.value and ant.antType == Model.AntType.SARBAAZ.value:
                        near_scorpions += 1
        if near_scorpions < 3:
            return Model.Direction.CENTER
        return ret

    def choose_best_strategy(self):
        # this will probably cause some bugs!
        if self.stays_in_group is None:
            if self.grid.chat_box_reader.get_now_turn() <= 10:
                self.stays_in_group = False
            elif randint(1, 10) <= 4:
                self.stays_in_group = True
            else:
                self.stays_in_group = False

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
