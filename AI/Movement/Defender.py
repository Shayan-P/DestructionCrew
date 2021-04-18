from random import shuffle

from AI.Movement import *
from .MovementStrategy import MovementStrategy
from AI.Grid import Grid, Cell
from AI.Grid.Cell import get_random_directions
import Model


class Defender(MovementStrategy):
    def __init__(self, base_ant):
        super(Defender, self).__init__(base_ant)

    def get_direction(self):
        cell = self.get_random_cell_near_base()
        if cell is None:
            return Model.Direction.CENTER
        return self.go_to(cell)

    def get_random_cell_near_base(self):
        print("\n\n", "im alive")
        candidates = self.grid.get_empty_adjacents(self.get_base_cell())
        print("\n\n", self.get_base_cell().x, self.get_base_cell().y)
        shuffle(candidates)
        return None if len(candidates) == 0 else candidates[0]
