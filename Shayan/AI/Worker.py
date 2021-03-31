from Model import *
import random


class Worker:
    def __init__(self, game):
        self.game = game

    def get_message(self):
        return "man worker am", 10

    def get_move(self):
        return Direction.RIGHT.value
