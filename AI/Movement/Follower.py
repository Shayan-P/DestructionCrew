from AI.Movement import *
from .MovementStrategy import MovementStrategy
from AI.Grid import Grid, Cell
from AI.Grid.Cell import get_random_directions
import Model


class Follower(MovementStrategy):
	def __init__(self, base_ant):
		super(Follower, self).__init__(base_ant)

	def get_direction(self):
		cell = self.get_closest_worker()
		if cell is None:
			return get_random_directions()[0]
		return self.go_to(cell)

	def get_closest_worker(self) -> Cell:
		best_cell = None
		best_distance = 0
		for cell in Grid.get_all_cells():
			if self.grid.is_unknown(cell) or len(self.grid.get_cell_ants(cell)) == 0:
				continue
			new_distance = self.grid.expected_distance(self.get_now_pos_cell(), cell)
			for ant in self.grid.get_cell_ants(cell):
				if ant.antTeam == Model.AntTeam.ALLIED.value \
						and ant.antType == Model.AntType.KARGAR.value \
						and (best_cell is None or best_distance > new_distance):
					best_cell = cell
					best_distance = new_distance
		return best_cell
