# from .BaseNews import BaseNews
from settings import READABLE_CHAT_BOX


def printable_ord(c):
	if ord('a') <= ord(c) <= ord('z'):
		return ord(c) - ord('a')
	if ord('A') <= ord(c) <= ord('Z'):
		return 26 + ord(c) - ord('A')
	if ord('0') <= ord(c) <= ord('9'):
		return 52 + ord(c) - ord('0')
	if c == '_':
		return 62
	if c == '!':
		return 63


def printable_chr(ind):
	if 0 <= ind < 26:
		return chr(ord('a') + ind)
	if 26 <= ind < 52:
		return chr(ord('A') + ind - 26)
	if 52 <= ind < 62:
		return chr(ord('0') + ind - 52)
	if ind == 62:
		return '_'
	if ind == 63:
		return '!'


def str_to_bin(char):
	res = ""
	if READABLE_CHAT_BOX:
		asci = printable_ord(char)
		for i in range(6):
			res = str(asci % 2) + res
			asci //= 2
	else:
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
		BYTE_SIZE = 6 if READABLE_CHAT_BOX else 8
		return len(self.message) + new.message_size() <= BYTE_SIZE * self.limit

	def write(self, mes, bits):
		res = ""
		for i in range(bits):
			res = str(mes % 2) + res
			mes //= 2
		self.message += res

	def get_message(self) -> str:
		res = ""
		if READABLE_CHAT_BOX:
			while len(self.message) % 6 != 0:
				self.message += "0"
			for i in range(0, len(self.message), 6):
				res += printable_chr(int(self.message[i: i + 6], 2))
		else:
			while len(self.message) % 8 != 0:
				self.message += "0"
			for i in range(0, len(self.message), 8):
				res += chr(int(self.message[i: i + 8], 2))
		return res


"""
don't use any of this functions. they are just helper classes for ChatBox.py
"""