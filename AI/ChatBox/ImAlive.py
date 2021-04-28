from .BaseNews import BaseNews
from .MessageHandlers import Reader, Writer
from Model import Cell as ModelCell
from AI.Config import Config
from AI.Grid.Cell import Cell as GridCell


class ImAlive(BaseNews):
	huffman_prefix = "00000000"  # too big?

	def __init__(self, is_worker, ant_id):
		super().__init__()
		self.ant_id = ant_id
		self.is_worker = is_worker

	def __str__(self):
		return f"ImAlive id:{self.ant_id} worker:{self.is_worker}"

	def get_priority(self):
		return 2

	def message_size(self):
		return len(ImAlive.huffman_prefix) + 7 + 1

	def encode(self, writer: Writer):
		writer.write(int(self.huffman_prefix, 2), len(self.huffman_prefix))
		writer.write(self.ant_id, 7)
		writer.write(int(self.is_worker), 1)

	@staticmethod
	def decode(reader: Reader) -> BaseNews:
		ant_id = reader.read(7)
		is_worker = bool(reader.read(1))
		return ImAlive(is_worker=is_worker, ant_id=ant_id)


"""
initialize it with cell that you want to report

use get_cell() to get Model.Cell of that cell (Maybe some data is unknown and set as None)

don't use another functions
"""