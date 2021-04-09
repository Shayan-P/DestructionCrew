from .MessageHandlers import Reader, Writer

class BaseNews:
	huffman_prefix = ""

	def __init__(self):
		self.priority: int = 0
		self.turn = 0

	def message_size(self) -> int:
		return 0

	def encode(self, writer: Writer):
		pass

	def get_priority(self) -> int:
		return self.priority

	def decode(self, reader: Reader):
		pass
