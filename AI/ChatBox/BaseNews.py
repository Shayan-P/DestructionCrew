from .MessageHandlers import Reader, Writer


class BaseNews:
	huffman_prefix = ""

	def __init__(self):
		self.priority: int = 0
		self.turn = 0

	def message_size(self) -> int:
		NotImplementedError

	def encode(self, writer: Writer):
		NotImplementedError

	def decode(self, reader: Reader):
		# todo
		NotImplementedError

	def get_priority(self) -> int:
		return self.priority

