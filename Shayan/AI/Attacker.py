from Model import *
import random


class Attacker:
    def __init__(self, game):
        self.game = game
    
    def get_message(self):
        return "man attacker am", 10

    def get_move(self):
        return Direction.LEFT.value
#        return random.choice(list(Direction)).value

