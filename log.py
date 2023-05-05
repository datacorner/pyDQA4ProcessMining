import logging
from logging.handlers import RotatingFileHandler
import constants as C

class log:
    def __init__(self, loggerName):
        self.__logger = logging.getLogger(loggerName)
        logHandler = logging.handlers.RotatingFileHandler(C.TRACE_FILENAME, mode="a", maxBytes= 100000, backupCount= 1 , encoding=C.ENCODING)
        logHandler.setFormatter(logging.Formatter(C.TRACE_FORMAT))
        self.__logger.setLevel(C.TRACE_LEVEL)
        self.__logger.addHandler(logHandler)

    def display(self, message):
        print(message)
    
    def buildMessage(self, _msg):
        final_message = ""
        for msg in _msg:
            final_message += str(msg)
        return final_message
    
    def info(self, *message):
        final_message = self.buildMessage(message)
        self.display("Info> " + final_message)
        self.__logger.info(final_message)

    def error(self, *message):
        final_message = self.buildMessage(message)
        self.display("Error> " + final_message)
        self.__logger.error(final_message)

    def debug(self, *message):
        final_message = self.buildMessage(message)
        self.display("Debug> " + final_message)
        self.__logger.debug(final_message)