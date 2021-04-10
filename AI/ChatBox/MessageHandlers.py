# from .BaseNews import BaseNews


def str_to_bin(char):
	res = ""
	asci = ord(char)
	for i in range(8):
		res = str(asci % 2) + res
		asci //= 2
	return res


class Reader:
	def __init__(self, message: str):
		self.message = ""
		for c in message:
			self.message += str_to_bin(c)
		self.pointer = 0

	def read(self, count):
		assert count + self.pointer <= len(self.message)
		mes = int(self.message[self.pointer:self.pointer + count], 2)
		self.pointer += count
		return mes

	def read_bit(self):
		self.pointer += 1
		return self.message[self.pointer - 1]

	def EOF(self) -> bool:
		return self.pointer == len(self.message)


class Writer:
	def __init__(self, limit):
		self.message = ""
		self.limit = limit

	def enough_space(self, new) -> bool:
		return len(self.message) + new.message_size() <= self.limit

	def write(self, mes, bits):
		res = ""
		for i in range(bits):
			res = str(mes % 2) + res
			mes //= 2
		self.message += res

	def get_message(self) -> str:
		res = ""
		while len(self.message) % 8 == 0:
			self.message += "0"

		for i in range(0, len(self.message), 8):
			res += chr(int(self.message[i: i + 8], 2))
		return res
