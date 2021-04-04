from Model import *


class Attacker:
    def __init__(self, game):
        self.game = game
        self.counter = 0
    
    def get_message(self):
        return f"man attacker am in turn f{self.counter}", 1

    def get_move(self):
        return Direction.LEFT.value

