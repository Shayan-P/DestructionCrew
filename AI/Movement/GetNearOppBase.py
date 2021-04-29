from AI.Movement import *
from .MovementStrategy import MovementStrategy
from AI.Grid import Grid, Cell
from AI.Choosing import soft_max_choose
from AI.Config import Config
from Model import Direction

from random import random, randint

class GetNearOpponentBase(MovementStrategy):
	def __init__(self, base_ant):
		super(GetNearOpponentBase, self).__init__(base_ant)
		self.delay = randint(2, self.base_ant.near_scorpions(1) + 1)

	def cell_near_opponent_base(self):
		opponent_base = self.base_ant.grid.expected_opponent_base()
		candid = None
		for cell in Grid.get_all_cells():
			if self.grid.unknown_graph.no_path(self.get_now_pos_cell(), cell):  # changed to unknown graph
				continue
			if candid is None or opponent_base.manhattan_distance(cell) < opponent_base.manhattan_distance(candid):
				candid = cell
		return candid

	def get_direction(self):
		self.delay -= 1
		if self.delay > 0:
			return Direction.CENTER
		return self.go_to(self.cell_near_opponent_base(), graph=self.grid.unknown_graph)

	def change_grid_coffs(self):
		self.grid.set_coffs(hate_known=10, opponent_base_fear=0, fight_fear=0)
		# opponent_base_fear must be 0. or we won't get close to it.
