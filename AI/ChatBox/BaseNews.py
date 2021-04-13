from .MessageHandlers import Reader, Writer


class BaseNews:
	huffman_prefix = ""

	def __init__(self):
		self.priority: int = 0
		self.turn = 10000
		# turn 10000 should mean that it is this turn
		# todo fix this?

	def get_turn(self):
		return self.turn

	def message_size(self) -> int:
		pass

	def encode(self, writer: Writer):
		NotImplementedError

	@staticmethod
	def decode(reader: Reader):
		pass

	def get_priority(self) -> int:
		return self.priority

