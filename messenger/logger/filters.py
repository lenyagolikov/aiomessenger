import logging


class MegaHandler(logging.Handler):
    def __init__(self, filename):
        logging.Handler.__init__(self)
        self.filename = filename

    def emit(self, record):
        message = self.format(record)
        with open(self.filename, "a") as file:
            file.write(message + "\n")


class DebugFilter(logging.Filter):
    def filter(self, record):
        return record.levelname == "DEBUG"


class ErrorFilter(logging.Filter):
    def filter(self, record):
        return record.levelname == "ERROR"
