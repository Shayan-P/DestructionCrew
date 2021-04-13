from typing import Tuple
from .MovementStrategy import MovementStrategy
from AI.Cell import Cell, DIRECTIONS
from .. import Grid
import Model

class Follower(MovementStrategy):
	def __init__(self, base_ant):
		super(Follower, self).__init__(base_ant)
	
	def get_direction(self):
		self.base_ant.pre_move()
		cell: Cell = self.get_closest_worker(self.base_ant.get_now_pos_cell())
		if cell is None:
			return DIRECTIONS[0]
		return self.go_to(cell)
	
	def get_closest_worker(self, source: Cell) -> Cell:
		self.grid.known_graph.precalculate_source(source)
		best_cell = None
		for x in range(self.grid.width):
			for y in range(self.grid.height):
				cell = Cell(x, y)
				if self.grid.is_unknown(cell) or len(self.grid.get_cell_ants(cell)) == 0:
					continue
				for ant in self.grid.get_cell_ants(cell):
					if ant.antTeam == Model.AntTeam.ALLIED.value \
					and ant.antType == Model.AntType.KARGAR.value \
					and (best_cell is None or best_cell.distance > self.grid.known_graph.get_vertex(cell).distance):
						best_cell = self.grid.known_graph.get_vertex(cell)
		return best_cell.cell