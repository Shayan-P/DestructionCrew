from AI.Movement import *
from .MovementStrategy import MovementStrategy
from AI.Grid import Grid, Cell
from AI.Choosing import soft_max_choose


class AloneSpy(MovementStrategy):
	def __init__(self, base_ant):
		super(AloneSpy, self).__init__(base_ant)
		self.previous_purpose = None  # use this todo
		# you can remove this

	def get_not_crowded_cell(self):
		candidates = {}
		for cell in Grid.get_all_cells():
			if self.grid.known_graph.no_path(self.get_now_pos_cell(), cell):
				continue
			score = 0
			for dx in range(-5, 6):
				for dy in range(-5, 6):
					another_cell = cell.move_to(dx, dy)
					dis = abs(dx) + abs(dy)
					if dis <= 5:
						score += (6-dis) * self.grid.get_crowded(another_cell)
			candidates[cell] = score
		return soft_max_choose(candidates)

	def get_direction(self):
		return self.go_to(self.get_not_crowded_cell())

	def change_grid_coffs(self):
		self.grid.set_coffs(hate_known=10, opponent_base_fear=5, fight_fear=3, scorpion_fear=5)
