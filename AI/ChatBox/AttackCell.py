from .BaseNews import BaseNews
from .MessageHandlers import Reader, Writer


class AttackCell(BaseNews):
	huffman_prefix = "010"

	def __init__(self, x=None, y=None):
		super().__init__()
		self.x = x
		self.y = y

	def get_x(self):
		return self.x

	def get_y(self):
		return self.y

	def message_size(self) -> int:
		return len(AttackCell.huffman_prefix) + 12

	def get_priority(self):
		return 2

	def encode(self, writer: Writer):
		writer.write(int(self.huffman_prefix, 2), len(self.huffman_prefix))
		writer.write(self.x, 6)
		writer.write(self.y, 6)

	@staticmethod
	def decode(reader: Reader) -> BaseNews:
		x = reader.read(6)
		y = reader.read(6)
		return AttackCell(x, y)


"""
initialize it with x, y of cell that you saw

use get_x()/get_y() to get x/y of that cell

don't use another functions
"""