from .BaseNews import BaseNews
from .MessageHandlers import Reader, Writer
from Model import Cell as ModelCell


class ViewCell(BaseNews):
	huffman_prefix = "1"

	def __init__(self, cell: ModelCell):
		super().__init__()
		self.cell: ModelCell = cell

	def message_size(self) -> int:
		return len(self.huffman_prefix) + 12 + 2  # prefix (x, y) type

	def get_priority(self):
		return 5

	def encode(self, writer: Writer):
		writer.write(int(self.huffman_prefix, 2), len(self.huffman_prefix))
		writer.write(self.cell.x, 6)
		writer.write(self.cell.y, 6)
		writer.write(self.cell.type, 2)

	def decode(self, reader: Reader):
		x = reader.read(6)
		y = reader.read(6)
		cell_type = reader.read(6)
		self.cell = ModelCell(x, y, cell_type, None, None)
