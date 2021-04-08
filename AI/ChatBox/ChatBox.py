import BaseNews

queueNews = []


def add_news(news):
    queueNews.append(news)


def flush():
    ret = ""
    for new in queueNews:
        ret += new.encode()
    return ret
