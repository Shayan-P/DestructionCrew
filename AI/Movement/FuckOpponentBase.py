from AI.Movement import *
from .MovementStrategy import MovementStrategy
from AI.Grid import Grid, Cell
from AI.Choosing import soft_max_choose
from AI.Config import Config


class FuckOpponentBase(MovementStrategy):
	def __init__(self, base_ant):
		super(FuckOpponentBase, self).__init__(base_ant)

	def cell_near_opponent_base(self):
		opponent_base = self.base_ant.grid.expected_opponent_base()
		candid = None
		for cell in Grid.get_all_cells():
			if self.grid.known_graph.no_path(self.get_now_pos_cell(), cell):
				continue
			if candid is None or opponent_base.manhattan_distance(cell) < opponent_base.manhattan_distance(candid):
				candid = cell
		return candid
		# this has some problems. maybe we get trapped! if we cannot get closer to base this way todo

	def get_direction(self):
		# momken nist becharkhim dor khodemoon? behtare ke fix bashe koja mirim. na inke taghir kone todo
		return self.go_to(self.cell_near_opponent_base())
