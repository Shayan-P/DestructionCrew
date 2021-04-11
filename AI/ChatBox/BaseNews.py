from .MessageHandlers import Reader, Writer


class BaseNews:
	huffman_prefix = ""

	def __init__(self):
		self.priority: int = 0
		self.turn = 0

	def message_size(self) -> int:
		pass

	def encode(self, writer: Writer):
		NotImplementedError

	@staticmethod
	def decode(reader: Reader):
		# todo
		pass

	def get_priority(self) -> int:
		return self.priority

