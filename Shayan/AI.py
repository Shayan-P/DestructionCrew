from Model import *
import random

from Utils import get_logger

logger = get_logger()


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
        logger.info("here we are")
        self.message = "hello python"
        self.value = random.randint(1,10)
        self.direction = random.choice(list(Direction)).value
#        self.direction = Direction.UP.value
        return self.message, self.value, self.direction
