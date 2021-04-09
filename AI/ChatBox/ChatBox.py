from .BaseNews import BaseNews

def str_to_bin(char):
	res = ""
	asci = ord(char);
	for i in range(8):
		res = str(i % 2) + res;
		i /= 2;
	return res;

class Reader:
	def __init__(self, message):
		self.message = ""
		for c in message:
			self.message += str_to_bin(c);
		self.pointer = 0

	def read(self, count):
		assert count + self.pointer <= len(message)			 
		mes = int(self.message[self.pointer, self.pointer + count], 2)
		self.pointer += count
		return mes;

class Writer:
	def __init__(self):
		self.message = "";	

	def write(self, mes, len):
		res = ""
		for i in range(len):
			res = str(i % 2) + res;
			i /= 2;
		self.message += res;

	def get_message(self):
		res = ""
		while(len(self.message) <= 256):
			self.message += "0"
		
		for i in range(0, 256, 8):
			res += chr(int(s[i : i + 8], 2));
		return res

class ChatBox:
	def __init__(self):
		self.queueNews = []

	def report(self, news: BaseNews):
		self.queueNews.append(news)

	def listen(self):
		pass

	def flush(self):
		ret = Writer();
		ret = "".join([new.encode() for new in self.queueNews])
		for new in self.queueNews:
			new.encode(ret)

		self.queueNews = []
		return ret.get_message()
