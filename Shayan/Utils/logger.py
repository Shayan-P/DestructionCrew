from logging import handlers, getLogger, Formatter, DEBUG
import os
from settings import LOG_PATH
import json


def get_logger():
    logger = getLogger()
    handler = handlers.RotatingFileHandler(os.path.join(LOG_PATH, str(log_id) + '.log'), 'a', maxBytes=10 * 1000 * 1000)
    formatter = Formatter(
        '%(asctime)s %(name)-12s %(levelname)-8s %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(DEBUG)
    return logger


def set_config(config):
    with open(os.path.join(LOG_PATH, 'config.json'), 'w') as f:
        f.write(json.dumps(config))


def get_config():
    with open(os.path.join(LOG_PATH, 'config.json'), 'r') as f:
        return json.loads(f.read())


log_id = get_config()['count']
set_config({'count': log_id+1})
