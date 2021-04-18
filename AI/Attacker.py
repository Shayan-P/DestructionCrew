from .BaseAnt import BaseAnt
from .Movement import Explore, Follower, Defender


class Attacker(BaseAnt):
    def __init__(self, game):
        super(Attacker, self).__init__(game)
        self.movement = Defender(self)

    def choose_best_strategy(self):
        if self.previous_strategy is Follower:
            return Follower
        if self.previous_strategy is Defender:
            return Defender
        #if self.game.alive_turn <= 3 and self.grid.chat_box_reader.get_now_turn() > 15:
         #   return Follower
        return Explore
