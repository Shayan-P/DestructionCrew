from .BaseAnt import BaseAnt
from .Movement import Explore, Follower, Defender, GrabAndReturn, GoCamp
from AI.Config import Config


class Attacker(BaseAnt):
    def __init__(self, game):
        super(Attacker, self).__init__(game)
        self.movement = Defender(self)

    def choose_best_strategy(self):
        # if there are a little unknown cells stop exploring todo
        # return GoCamp
        if self.previous_strategy is None:
<<<<<<< HEAD
            self.previous_strategy = Explore
            self.previous_strategy_object = Explore(self)
        # if self.game.ant.currentResource.value > Config.ant_max_rec_amount * 0.5:
        #     return GoCamp
        # # momkene ye chiz kam dastet bashe baad be khatere oon natooni chizi bardari. todo fix this
        # if (self.previous_strategy is not GoCamp) and GoCamp(self).is_really_good():
        #     return GoCamp
        if self.previous_strategy is GoCamp:
=======
            self.previous_strategy = GoCamp
            self.previous_strategy_object = GoCamp(self)

        if self.game.ant.currentResource.value > Config.ant_max_rec_amount * 0.5:
>>>>>>> af3e7df89d3f5cab45573baf8354e532c45b2009
            return GoCamp
        if GoCamp(self).is_not_good():
            return Explore
        # if self.previous_strategy is Explore:
        #     return Explore
        return GoCamp