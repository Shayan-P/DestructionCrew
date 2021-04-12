from Model import *
from .Attacker import Attacker
from .Worker import Worker
from Utils import logger
# just remove this and everything will be printed in console


class AI:
    def __init__(self):
        # Current Game State
        self.game: Game = None

        # Answer
        self.message: str = None
        self.direction: int = None
        self.value: int = None

    """
    Return a tuple with this form:
        (message: str, message_value: int, message_direction: int)
    check example
    """

    def turn(self) -> (str, int, int):
        global turn_count
        if turn_count == 0:
            init(self.game)
        turn_count += 1  # store the turns
        ant = get_ant(self.game.antType)
        ant.game = self.game
        self.direction = ant.get_move()
        self.message, self.value = ant.get_message_and_priority()
        # print("turn ", self.message, self.value, self.direction)
        return self.message, self.value, self.direction.value


turn_count = 0
worker = None
attacker = None


def init(game):
    global worker, attacker
    worker = Worker(game)
    attacker = Attacker(game)


def get_ant(ant_type):
    if ant_type == AntType.SARBAAZ.value:
        return attacker
    else:
        return worker
