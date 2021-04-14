from copy import deepcopy

from .BaseNews import BaseNews
from .MessageHandlers import Reader, Writer
from Model import Cell as ModelCell


class ViewScorpion(BaseNews):
	huffman_prefix = "0001"

	def __init__(self, cell: ModelCell = None):
		super().__init__()
		self.cell: ModelCell = deepcopy(cell)

	def get_cell(self) -> ModelCell:
		return self.cell

	def message_size(self) -> int:
		return len(self.huffman_prefix) + 12  # prefix (x, y) type

	def get_priority(self):
		# todo
		return 7

	def encode(self, writer: Writer):
		writer.write(int(self.huffman_prefix, 2), len(self.huffman_prefix))
		writer.write(self.cell.x, 6)
		writer.write(self.cell.y, 6)

	@staticmethod
	def decode(reader: Reader) -> BaseNews:
		x = reader.read(6)
		y = reader.read(6)
		cell = ModelCell(x, y, None, None, None)
		return ViewScorpion(cell)

"""
initialize it with cell that you want to report

use get_cell() to get Model.Cell of that cell (only x, y is known)

don't use another functions
"""