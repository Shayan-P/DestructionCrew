from copy import deepcopy

from .BaseNews import BaseNews
from .MessageHandlers import Reader, Writer
from Model import Cell as ModelCell
from AI.Config import Config
from AI.Grid.Cell import Cell as GridCell


class FightZone(BaseNews):
	huffman_prefix = "11"

	my_k = 3
	opp_k = 1

	def __init__(self, my_cell: ModelCell, opp_cell: ModelCell):
		super().__init__()
		self.cell: GridCell = None

		if opp_cell is None:
			self.cell = GridCell.from_model_cell(my_cell)
			return

		view_range = Config.view_distance
		my = GridCell.from_model_cell(my_cell)
		opp = GridCell.from_model_cell(opp_cell)

		min_dis = None
		for dx in range(-view_range, view_range + 1):
			for dy in range(-view_range, view_range + 1):
				this_cell = my.move_to(dx, dy)
				dis = max(FightZone.my_k * this_cell.manhattan_distance(my), FightZone.opp_k * this_cell.manhattan_distance((opp)) )
				if (self.cell is None) or (dis < min_dis):
					min_dis = dis
					self.cell = this_cell
		# print(Config.map_width, Config.map_height)
		# print("!! (", my.x, ",", my.y,") + (", opp.x,",",opp.y,") -> (", self.cell.x, ", ", self.cell.y, ")")
		# assert min_dis <= 3

	def get_cell(self) -> ModelCell:
		return ModelCell(self.cell.x, self.cell.y, None, None, None)

	def message_size(self) -> int:
		return len(self.huffman_prefix) + 12  # prefix (x, y) type

	def get_priority(self):
		return 1

	def encode(self, writer: Writer):
		# print("Shaash")
		# print("sending", self.cell.x, self.cell.y)
		writer.write(int(self.huffman_prefix, 2), len(self.huffman_prefix))
		writer.write(self.cell.x, 6)
		writer.write(self.cell.y, 6)

	@staticmethod
	def decode(reader: Reader) -> BaseNews:
		# print("Ann")
		x = reader.read(6)
		y = reader.read(6)
		# print("receiving", x, y)
		cell = ModelCell(x, y, None, None, None)
		return FightZone(cell, None)


"""
initialize it with cell that you want to report

use get_cell() to get Model.Cell of that cell (Maybe some data is unknown and set as None)

don't use another functions
"""