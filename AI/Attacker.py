from Model import *
from Utils import get_logger

logger = get_logger()


class Attacker:
    def __init__(self, game):
        self.game = game
        self.counter = 0
    
    def get_message(self):
        return "⿈⿈⿈⿈⿈⿈⿈⿈⿈⿈⿈⿈⿈⿈⿈⿈⿈⿈⿈⿈⿈⿈⿈⿈⿈⿈⿈⿈⿈⿈⿈⿈", 1

    def get_move(self):
        arr = [chat.text for chat in self.game.chatBox.allChats]
#        logger.log(arr)
        print(arr)
        return Direction.LEFT.value

