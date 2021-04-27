from .BaseNews import BaseNews
from .MessageHandlers import Reader, Writer
from AI.Grid.Cell import Cell as GridCell


class SafeDangerCell(BaseNews):
	huffman_prefix = "010"

	def __init__(self, cell: GridCell, danger=False):
		super().__init__()
		self.cell = cell
		self.danger = danger

	def __str__(self):
		if self.danger:
			return f"Danger{str(self.cell)}"
		else:
			return f"Safe{str(self.cell)}"

	def get_cell(self):
		return self.cell

	def get_danger(self):
		return self.danger

	def message_size(self) -> int:
		return len(SafeDangerCell.huffman_prefix) + 12 + 1

	def get_priority(self):
		return 2

	def encode(self, writer: Writer):
		writer.write(int(self.huffman_prefix, 2), len(self.huffman_prefix))
		writer.write(self.cell.x, 6)
		writer.write(self.cell.y, 6)
		writer.write(int(self.danger), 1)

	@staticmethod
	def decode(reader: Reader) -> BaseNews:
		x = reader.read(6)
		y = reader.read(6)
		danger = bool(reader.read(1))
		return SafeDangerCell(GridCell(x, y), danger)


"""
initialize it with x, y of cell that you saw

use get_x()/get_y() to get x/y of that cell

don't use another functions
"""