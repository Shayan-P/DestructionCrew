from copy import deepcopy

from .BaseNews import BaseNews
from .MessageHandlers import Reader, Writer
from Model import Cell as ModelCell
from random import randint


class Gathering(BaseNews):
	huffman_prefix = "0011"

	priority_size = 10
	def __init__(self, cell: ModelCell, priority=-1, life_time=6):
		super().__init__()
		self.cell: ModelCell = deepcopy(cell)
		if priority == -1:
			self.priority = randint(0, 2**Gathering.priority_size - 1)
		self.life_time = life_time

	def get_cell(self) -> ModelCell:
		return self.cell

	def __str__(self):
		return f"meet({self.cell.x}, {self.cell.y})"

	def message_size(self) -> int:
		return len(self.huffman_prefix) + 12 + Gathering.priority_size + 4  # prefix (x, y) priority expired

	def get_priority(self):
		return 100

	def get_new_priority(self):
		return self.priority

	def encode(self, writer: Writer):
		# print("ENCODING ", self.cell.x, self.cell.y)
		writer.write(int(self.huffman_prefix, 2), len(self.huffman_prefix))
		writer.write(self.cell.x, 6)
		writer.write(self.cell.y, 6)
		writer.write(self.priority, Gathering.priority_size)
		writer.write(self.life_time, 4)

	@staticmethod
	def decode(reader: Reader) -> BaseNews:
		x = reader.read(6)
		y = reader.read(6)
		priority = reader.read(Gathering.priority_size)
		life_time = reader.read(4)
		cell = ModelCell(x, y, None, None, None)
		return Gathering(cell, priority, life_time)


"""
initialize it with cell that you want to report

use get_cell() to get Model.Cell of that cell (Maybe some data is unknown and set as None)

don't use another functions
"""