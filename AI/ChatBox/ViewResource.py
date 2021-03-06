from .BaseNews import BaseNews
from .MessageHandlers import Reader, Writer
from Model import Cell as ModelCell
from Model import CellType
from copy import deepcopy


class ViewResource(BaseNews):
	huffman_prefix = "011"

	def __init__(self, cell: ModelCell):
		super().__init__()
		self.cell: ModelCell = deepcopy(cell)

	def __str__(self):
		return f"RS({self.cell.x},{self.cell.y}):{self.cell.resource_value}"

	def get_cell(self) -> ModelCell:
		return self.cell

	def message_size(self) -> int:
		return len(self.huffman_prefix) + 12 + 2 + 8  # prefix (x, y) type value

	def get_priority(self):
		return 4

	def encode(self, writer: Writer):
		writer.write(int(self.huffman_prefix, 2), len(self.huffman_prefix))
		writer.write(self.cell.x, 6)
		writer.write(self.cell.y, 6)
		# print("resource value -> ", self.cell.resource_value)
		# need to test carefully todo
		self.cell.resource_value = max(0, self.cell.resource_value)
		writer.write(self.cell.resource_type, 2)
		writer.write(min(255, self.cell.resource_value), 8)

	@staticmethod
	def decode(reader: Reader) -> BaseNews:
		x = reader.read(6)
		y = reader.read(6)
		cell_resource_type = reader.read(2)
		cell_resource_value = reader.read(8)
		cell = ModelCell(x, y, CellType.EMPTY, cell_resource_value, cell_resource_type)
		return ViewResource(cell)

"""
initialize it with cell that you want to report

use get_cell() to get Model.Cell of that cell (Maybe some data is unknown and set as None)

don't use another functions
"""