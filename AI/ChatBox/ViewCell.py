from copy import deepcopy

from .BaseNews import BaseNews
from .MessageHandlers import Reader, Writer
from Model import Cell as ModelCell


class ViewCell(BaseNews):
	huffman_prefix = "10"

	def __init__(self, cell: ModelCell):
		super().__init__()
		self.cell: ModelCell = deepcopy(cell)

	def __str__(self):
		return f"VC{self.cell.x},{self.cell.y}"

	def get_cell(self) -> ModelCell:
		return self.cell

	def message_size(self) -> int:
		return len(self.huffman_prefix) + 12 + 1  # prefix (x, y) type

	def get_priority(self):
		return 1

	def encode(self, writer: Writer):
		# print("ENCODING ", self.cell.x, self.cell.y)
		writer.write(int(self.huffman_prefix, 2), len(self.huffman_prefix))
		writer.write(self.cell.x, 6)
		writer.write(self.cell.y, 6)
		writer.write(max(0, self.cell.type - 1), 1)

	@staticmethod
	def decode(reader: Reader) -> BaseNews:
		x = reader.read(6)
		y = reader.read(6)
		cell_type = reader.read(1)
		cell = ModelCell(x, y, cell_type + 1, None, None)
		return ViewCell(cell)


"""
initialize it with cell that you want to report

use get_cell() to get Model.Cell of that cell (Maybe some data is unknown and set as None)

don't use another functions
"""