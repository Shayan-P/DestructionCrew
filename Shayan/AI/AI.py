from Model import *
from .Attacker import Attacker
from .Worker import Worker
from Utils import get_logger


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
        (message: str, message_value: int, message_dirction: int)
    check example
    """

    def turn(self) -> (str, int, int):
        try:
            if FIRST_MOVE:
                init(self.game)
            ant = get_ant(self.game.antType)
            ant.game = self.game
            self.message, self.value = ant.get_message()
            self.direction = ant.get_move()
            logger.info(str([self.message, self.value, self.direction]))
            return self.message, self.value, self.direction
        except Exception as e:
            logger.error(e)


FIRST_MOVE = True

logger = get_logger()
worker = None
attacker = None


def init(game):
    global FIRST_MOVE, worker, attacker
    FIRST_MOVE = False
    worker = Worker(game)
    attacker = Attacker(game)


def get_ant(ant_type):
    if ant_type == 0:
        return attacker
    else:
        return worker
