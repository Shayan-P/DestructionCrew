from .BaseNews import BaseNews
from random import randint
from Model import Game, ChatBox
from .MessageHandlers import Reader, Writer

from .AttackCell import AttackCell

all_message_types : [BaseNews] = [AttackCell]


class ChatBoxWriter:
	def __init__(self, game: Game):
		self.queueNews: [BaseNews] = []
		self.game = game

	def report(self, news: BaseNews):
		self.queueNews.append(news)

	def flush(self) -> str:
		self.queueNews.sort(key = lambda new: new.get_priority(), reverse = True)
		# need to obtain from map configs
		ret = Writer(32)
		for new in self.queueNews:
			if(ret.enoughSpace(new)):
				new.encode(ret)

		self.queueNews = []

		return ret.get_message()

	def get_priority(self) -> int:
		return randint(1, 1000)


class ChatBoxReader:
	def __init__(self, box: ChatBox):
		self.news : [BaseNews] = []
		msg_readers = []
		for msg in box.allChats:
			msg_readers.append(Reader(msg.text))
		for reader in msg_readers:
			prefix = ""
			found = False
			while not reader.EOF():
				while (not reader.EOF()) and (prefix not in [new_type.huffman_prefix for new_type in all_message_types]):
					prefix += reader.read_bit()
					found = True
				if not found:
					continue
				message_type = None
				for new_type in all_message_types:
					if(prefix == new_type.huffman_prefix):
						message_type = new_type
				self.news.append(message_type().decode(reader))

	def get_X_news(self, new_type) -> [BaseNews]:
		msgs = []
		for new in self.news:
			if(type(new) == new_type):
				msgs.append(new)
		return msgs

	def get_attack_cell_news(self) -> [AttackCell]:
		return self.get_X_news(AttackCell)

