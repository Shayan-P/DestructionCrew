from .BaseAnt import BaseAnt
from .Movement import GrabAndReturn


class Worker(BaseAnt):
    def __init__(self, game):
        super(Worker, self).__init__(game)
        self.movement = GrabAndReturn(self)

    def get_message(self):
        return f"worker: I have yummy of type {self.game.ant.currentResource.type} with value" \
               f" {self.game.ant.currentResource.value}", 10

    def get_move(self):
        super(Worker, self).get_move()
        return self.movement.get_direction()
