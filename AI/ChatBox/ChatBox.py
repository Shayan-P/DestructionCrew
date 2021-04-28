from .BaseNews import BaseNews
from random import randint
from Model import ChatBox
from .MessageHandlers import Reader, Writer
from AI.Config import Config

from typing import List, Dict, Type

from .SafeDangerCell import SafeDangerCell
from .ViewCell import ViewCell
from .ViewScorpion import ViewScorpion
from .ViewOppBase import ViewOppBase
from .ViewResource import ViewResource
from .FightZone import FightZone
from .ImAlive import ImAlive
from .Gathering import Gathering

all_message_types: List[Type[BaseNews]] = BaseNews.__subclasses__()

for t1 in all_message_types:
	for t2 in all_message_types:
		if t1 is t2:
			continue
		ln = min(len(t1.huffman_prefix), len(t2.huffman_prefix))
		assert t1.huffman_prefix[:ln] != t2.huffman_prefix[:ln]


class ChatBoxWriter:
	def __init__(self):
		self.queue_news: [BaseNews] = []
		self.stuck_news: [BaseNews] = []
		self.last_turn_news: [BaseNews] = []
		self.limit = Config.max_com_length
		self.priority = 0
		self.turn = 1

	def update(self, turn, previous_news_in_chat_box: [BaseNews]):
		self.turn = turn
		last_turn_sent_news = set()
		for news in previous_news_in_chat_box:
			last_turn_sent_news.add(get_encoded_message(news))
		for news in self.last_turn_news:
			if get_encoded_message(news) not in last_turn_sent_news:
				self.stuck_news.append(news)

	def report(self, news: BaseNews):
		self.queue_news.append(news)

	def flush(self) -> str:
		self.queue_news.sort(key=lambda news: news.get_priority(), reverse=True)
		self.stuck_news.sort(key=lambda news: news.get_priority(), reverse=True)
		all_news = self.queue_news + self.stuck_news
		self.queue_news = []
		self.stuck_news = []
		self.last_turn_news = []
		# need to obtain from map configs
		self.priority = 0
		ret = Writer(self.limit)
		for new in all_news:
			if ret.enough_space(new):
				new.encode(ret)
				self.priority += new.get_priority()
				self.last_turn_news.append(new)
			else:
				# must
				self.stuck_news.append(new)
				print("cant report news: ", new)

		# todo
		# store the messages that ignored because of not enough space
		# return ""
		return ret.get_message()

	def get_priority(self) -> int:
		return self.turn * 10000 + self.priority


class ChatBoxReader:
	def __init__(self):
		self.last_check = 0
		self.news: Dict[ Type[BaseNews] , List[BaseNews] ] = {}
		self.latest_news: Dict[ Type[BaseNews] , List[BaseNews] ] = {}
		for news_type in all_message_types:
			self.news[news_type] = []

	def update(self, box: ChatBox):
		for news_type in all_message_types:
			self.latest_news[news_type] = []
		for msg in box.allChats:
			if(msg.turn <= self.last_check): # Already Added
				continue

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
				this_news.turn = msg.turn
				self.news[message_type].append(this_news)
				self.latest_news[message_type].append(this_news)
				# print("getting message with type: ", type(this_news))
		for msg in box.allChats:
			self.last_check = max(self.last_check, msg.turn)

	def get_now_turn(self):
		return self.last_check + 1

	def get_all_news(self, news_type: Type[BaseNews]) -> [BaseNews]:
		return self.news[news_type]

	def get_latest_news(self, news_type: Type[BaseNews]) -> [BaseNews]:
		return self.latest_news[news_type]

	def get_latest_news_all_types(self):
		ret = []
		for t in self.latest_news:
			ret += self.latest_news[t]
		return ret


def get_encoded_message(news: BaseNews):
	writer = Writer(Config.max_com_length)
	news.encode(writer)
	return writer.get_message()


def message_text_translator(text):
	reader = Reader(text)
	ret = ""
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
		ret += str(this_news) + " * "
	return ret


"""
ChatBoxWriter:
Build Once (optional: every turn)
Add All news with ChatBoxWriter.report(news) before flushing
at the end use ChatBoxWriter.flush to get coded message
and use ChatBoxWriter.get_priority() to get priority of message

ChatBoxReader:

ATTENTION: Build ONCE, update EVERY fucking turn !

you should pass game.chatBox to constructor
use ChatBoxReader.get_(name of news you need)_news() to get list of news of that type
"""