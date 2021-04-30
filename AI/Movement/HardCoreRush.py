from AI.Movement import *
from .MovementStrategy import MovementStrategy
from AI.Grid import Grid, Cell
from AI.Choosing import soft_max_choose
from AI.Config import Config
from random import random, randint, choice

from Model import Direction

class HardCoreRush(MovementStrategy):
	def __init__(self, base_ant):
		super(HardCoreRush, self).__init__(base_ant)
		self.destination = None
		self.delay = randint(1, 3)
		self.change_grid_coffs()

	def cell_near_opponent_base(self):
		pass

	def set_destination(self):
		opp_base = self.grid.expected_opponent_base
		candids = []
		for cell in self.grid.get_all_cells():
			if cell.manhattan_distance(opp_base) <= 6:
				continue
			if 8 < cell.manhattan_distance(opp_base):
				continue
			dis = self.grid.known_graph.get_shortest_distance(self.base_ant.get_now_pos_cell(), cell)
			if dis is None:
				continue
			if dis > Config.start_rape - Config.start_rush:
				continue
			candids.append(cell)
		if len(candids) == 0:
			return None
		return choice(candids)

	def go_near_opp_base(self):
		if self.destination is None:
			self.set_destination()
		if self.destination is None:
			return Direction.CENTER
		return self.go_to(self.destination)

	def rush_in(self):
		self.delay -= 1
		if self.delay > 0:
			return Direction.CENTER
		return self.go_to(self.grid.expected_opponent_base(), self.grid.simple_graph)

	def get_direction(self):
		if self.grid.chat_box_reader.get_now_turn() < Config.start_rape:
			return self.go_near_opp_base()
		return self.rush_in()

	def change_grid_coffs(self):
		self.grid.set_coffs(hate_known=0, opponent_base_fear=1, fight_fear=0)
		# opponent_base_fear must be 0. or we won't get close to it.
