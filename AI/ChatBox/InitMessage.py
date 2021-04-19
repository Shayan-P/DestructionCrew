from .BaseNews import BaseNews
from .MessageHandlers import Reader, Writer
from Model import Cell as ModelCell
from AI.Config import Config
from AI.Grid.Cell import Cell as GridCell


class InitMessage(BaseNews):
	# felan natoonestam prefix printable barash peyda konam ke chap she!
	huffman_prefix = "0000000000000000"

	init_message = "WeAreDestructionCrew.Heh!"

	def __init__(self):
		super().__init__()

	def get_priority(self):
		return 0

	def message_size(self):
		return len(InitMessage.huffman_prefix) + len(InitMessage.init_message) * 8

	def encode(self, writer: Writer):
		writer.write(int(self.huffman_prefix, 2), len(self.huffman_prefix))
		for c in InitMessage.init_message:
			writer.write(ord(c), 8)

	def __hash__(self):
		return hash(InitMessage.huffman_prefix, self.turn)

	@staticmethod
	def decode(reader: Reader) -> BaseNews:
		for c in InitMessage.init_message:
			cc = chr(reader.read(8))
			assert cc == c
		return InitMessage()


"""
initialize it with cell that you want to report

use get_cell() to get Model.Cell of that cell (Maybe some data is unknown and set as None)

don't use another functions
"""