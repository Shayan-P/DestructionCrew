import logging
import os
import json

from settings import LOG_PATH
from logging import handlers, Formatter


def get_logger():
    logger = logging.getLogger()
    handler = handlers.RotatingFileHandler(os.path.join(LOG_PATH, str(log_id) + '.log'), 'a', maxBytes=10 * 1000 * 1000)
    formatter = Formatter(
        '%(asctime)s %(name)-12s %(levelname)-8s %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(logging.DEBUG)
    return logger


def get_terminal_logger():
    logger = logging.getLogger()
    logger.addHandler(logging.StreamHandler())
    return logger


def set_config(config):
    with open(os.path.join(LOG_PATH, 'config.json'), 'w') as f:
        f.write(json.dumps(config))


def get_config():
    with open(os.path.join(LOG_PATH, 'config.json'), 'r') as f:
        return json.loads(f.read())


log_id = get_config()['count']
set_config({'count': log_id+1})
