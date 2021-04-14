from .BaseNews import BaseNews
from random import randint
from Model import ChatBox
from .MessageHandlers import Reader, Writer
from AI.Config import Config


all_message_types: [BaseNews] = BaseNews.__subclasses__()


class ChatBoxWriter:
	def __init__(self):
		self.queueNews: [BaseNews] = []
		self.limit = Config.max_com_length

	def report(self, news: BaseNews):
		self.queueNews.append(news)

	def flush(self) -> str:
		self.queueNews.sort(key=lambda news: news.get_priority(), reverse=True)
		# need to obtain from map configs
		ret = Writer(self.limit)
		for new in self.queueNews:
			if ret.enough_space(new):
				new.encode(ret)

		self.queueNews = []

		# todo
		# store the messages that ignored because of not enough space

		return ret.get_message()

	def get_priority(self) -> int:
		# todo fix priorities
		return randint(1, 1000)


class ChatBoxReader:
	def __init__(self, box: ChatBox):
		print("!!!!", len(all_message_types), " -> ", all_message_types)
		self.news: [BaseNews] = []
		self.my_turn = 0
		for msg in box.allChats:
			turn = msg.turn
			self.my_turn = max(self.my_turn, turn + 1)
			reader = Reader(msg.text)
			while not reader.EOF():
				prefix = ""
				while (not reader.EOF()) and (prefix not in [new_type.huffman_prefix for new_type in all_message_types]):
					prefix += reader.read_bit()
				if prefix not in [new_type.huffman_prefix for new_type in all_message_types]:
					continue
				message_type = None
				for new_type in all_message_types:
					if prefix == new_type.huffman_prefix:
						message_type = new_type
				this_news = message_type.decode(reader)
				this_news.turn = turn
				self.news.append(this_news)

	def get_now_turn(self):
		return self.my_turn
		# todo this may be wrong. there might be a case were chat box does not update. but probably it makes no problem

	def get_all_news(self) -> [BaseNews]:
		return self.news


"""
ChatBoxWriter:
Build Once (optional: every turn)
Add All news with ChatBoxWriter.report(news) before flushing
at the end use ChatBoxWriter.flush to get coded message
and use ChatBoxWriter.get_priority() to get priority of message

ChatBoxReader:

ATTENTION: Build EVERY fucking turn !

you should pass game.chatBox to constructor
use ChatBoxReader.get_(name of news you need)_news() to get list of news of that type
"""