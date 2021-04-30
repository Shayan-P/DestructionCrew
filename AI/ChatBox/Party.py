from copy import deepcopy

from .BaseNews import BaseNews
from .MessageHandlers import Reader, Writer
from Model import Cell as ModelCell
from random import randint


class Party(BaseNews):
	huffman_prefix = "00011"

	priority_size = 10
	def __init__(self, cell: ModelCell, age, ant_id):
		super().__init__()
		self.cell: ModelCell = deepcopy(cell)
		self.priority = 256 * age + ant_id

	def get_cell(self) -> ModelCell:
		return self.cell

	def __str__(self):
		return f"party({self.cell.x}, {self.cell.y})"

	def message_size(self) -> int:
		return len(self.huffman_prefix) + 12 + 16 # prefix (x, y) priority

	def get_priority(self):
		return self.priority

	def encode(self, writer: Writer):
		# print("ENCODING ", self.cell.x, self.cell.y)
		writer.write(int(self.huffman_prefix, 2), len(self.huffman_prefix))
		writer.write(self.cell.x, 6)
		writer.write(self.cell.y, 6)
		writer.write(self.priority, 16)

	@staticmethod
	def decode(reader: Reader) -> BaseNews:
		x = reader.read(6)
		y = reader.read(6)
		priority = reader.read(16)
		cell = ModelCell(x, y, None, None, None)
		return Party(cell, priority // 256, priority % 256)


"""
initialize it with cell that you want to report

use get_cell() to get Model.Cell of that cell (Maybe some data is unknown and set as None)

don't use another functions
"""