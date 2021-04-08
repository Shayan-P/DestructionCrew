from .BaseNews import BaseNews


class ChatBox:
    def __init__(self):
        self.queueNews = []

    def report(self, news: BaseNews):
        self.queueNews.append(news)

    def listen(self):
        pass

    def flush(self):
        ret = "".join([new.encode for new in self.queueNews])
        self.queueNews = []
        return ret
