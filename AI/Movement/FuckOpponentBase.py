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
			if self.grid.unknown_graph.no_path(self.get_now_pos_cell(), cell):  # changed to unknown graph
				continue
			if candid is None or opponent_base.manhattan_distance(cell) < opponent_base.manhattan_distance(candid):
				candid = cell
		return candid

	def get_best_path(self, cell_start: Cell, cell_end: Cell):
		if not self.grid.unknown_graph.no_path(cell_start, cell_end):
			return self.grid.unknown_graph.get_shortest_path(cell_start, cell_end)
		return None

	def get_direction(self):
		return self.go_to(self.cell_near_opponent_base())
