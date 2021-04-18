from .BaseNews import BaseNews
from random import randint
from Model import ChatBox
from .MessageHandlers import Reader, Writer
from AI.Config import Config

from .AttackCell import AttackCell
from .ViewCell import ViewCell
from .ViewScorpion import ViewScorpion
from .ViewOppBase import ViewOppBase
from .ViewResource import ViewResource
from .FightZone import FightZone
from .InitMessage import InitMessage


all_message_types: [BaseNews] = BaseNews.__subclasses__()

for t1 in all_message_types:
	for t2 in all_message_types:
		if t1 is t2:
			continue
		ln = min(len(t1.huffman_prefix), len(t2.huffman_prefix))
		assert t1.huffman_prefix[:ln] != t2.huffman_prefix[:ln]


class ChatBoxWriter:
	def __init__(self, turn = 1):
		self.queueNews: [BaseNews] = []
		self.limit = Config.max_com_length
		self.priority = 0
		self.turn = turn

	def report(self, news: BaseNews):
		self.queueNews.append(news)

	def flush(self) -> str:
		self.queueNews.sort(key=lambda news: news.get_priority(), reverse=True)
		# need to obtain from map configs
		self.priority = 0
		ret = Writer(self.limit)
		for new in self.queueNews:
			if ret.enough_space(new):
				new.encode(ret)
				self.priority += new.get_priority()

		self.queueNews = []

		# todo
		# store the messages that ignored because of not enough space
		# return ""
		return ret.get_message()

	def get_priority(self) -> int:
		return self.turn * 10000 + self.priority


class ChatBoxReader:
	def __init__(self, box: ChatBox):
		self.news: [BaseNews] = []
		self.my_turn = 1
		for msg in box.allChats:
			turn = msg.turn
			self.my_turn = max(self.my_turn, turn + 1)

		for msg in box.allChats:
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