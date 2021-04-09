from .BaseNews import BaseNews
from .MessageHandlers import Reader, Writer


class AttackCell(BaseNews):
	huffman_prefix = "001"

	def __init__(self, x=None, y=None):
		super().__init__()
		self.x = x
		self.y = y

	def message_size(self) -> int:
		return len(AttackCell.huffman_prefix) + 12

	def get_priority(self):
		return 0

	def encode(self, writer: Writer):
		writer.write(int(self.huffman_prefix, 2), len(self.huffman_prefix))
		writer.write(self.x, 6)
		writer.write(self.y, 6)

	def decode(self, reader: Reader):
		self.x = reader.read(6)
		self.y = reader.read(6)
