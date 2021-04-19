import os
import json
import sys

from settings import LOG_PATH, DEBUG

class Logger:
    def __init__(self, filename):
        self.console = sys.stdout
        self.file = open(filename, 'w')

    def write(self, message):
        message = str(message)
        self.console.write(message)
        self.file.write(message)

    def flush(self):
        self.console.flush()
        self.file.flush()


def set_config(config):
    with open(os.path.join(LOG_PATH, 'config.json'), 'w') as f:
        f.write(json.dumps(config))


def get_config():
    with open(os.path.join(LOG_PATH, 'config.json'), 'r') as f:
        return json.loads(f.read())


if DEBUG:
    log_id = get_config()['count']
    set_config({'count': log_id+1})

    logger = Logger(os.path.join(LOG_PATH, f"{log_id}.log"))
    sys.stdout = logger
    sys.stderr = logger

else:
    class DummyLogger:
        def __init__(self):
            pass

        def write(self, message):
            pass

        def flush(self):
            pass
    dummy_logger = DummyLogger()
    sys.stdout = dummy_logger
    sys.stderr = dummy_logger

