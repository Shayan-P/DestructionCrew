from typing import Tuple
from .MovementStrategy import MovementStrategy
from AI.Cell import Cell

class Follower(MovementStrategy):
	def __init__(self, base_ant):
		super(Follower, self).__init__(base_ant)
	
	def get_direction(self):
		self.base_ant.pre_move()
		return self.go_to(Cell(self.grid.get_closest_worker()))