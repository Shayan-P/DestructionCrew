from .BaseNews import BaseNews
from .MessageHandlers import Reader, Writer
from AI.Grid.Cell import Cell


class SafeDangerCell(BaseNews):
	huffman_prefix = "010"

	def __init__(self, cell, danger=False):
		super().__init__()
		self.x = cell.x
		self.y = cell.y
		self.danger = danger

	def get_x(self):
		return self.x

	def get_y(self):
		return self.y

	def get_danger(self):
		return self.danger

	def message_size(self) -> int:
		return len(SafeDangerCell.huffman_prefix) + 12 + 1

	def get_priority(self):
		return 2

	def encode(self, writer: Writer):
		writer.write(int(self.huffman_prefix, 2), len(self.huffman_prefix))
		writer.write(self.x, 6)
		writer.write(self.y, 6)
		writer.write(int(self.danger), 1)

	def __hash__(self):
		return hash(SafeDangerCell.huffman_prefix, self.turn, self.cell.x, self.cell.y, self.danger)

	@staticmethod
	def decode(reader: Reader) -> BaseNews:
		x = reader.read(6)
		y = reader.read(6)
		danger = bool(reader.read(1))
		return SafeDangerCell(Cell(x, y), danger)


"""
initialize it with x, y of cell that you saw

use get_x()/get_y() to get x/y of that cell

don't use another functions
"""