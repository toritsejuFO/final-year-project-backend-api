import os
import logging
from logging.handlers import RotatingFileHandler

# Disable flask's default logger
werkzeug_logger = logging.getLogger('werkzeug')
werkzeug_logger.disabled = True


# Setup application logging
if not os.path.exists('logs'):
    os.mkdir('logs')


# Replace default logger
stream_logger = logging.getLogger('stream')
stream_logger.setLevel(logging.DEBUG)
stream_handler = logging.StreamHandler()
stream_handler.setFormatter(logging.Formatter(
    '[%(asctime)s] - %(message)s'))
stream_logger.addHandler(stream_handler)


# To log application errors and exceptions
logger = logging.getLogger(__name__)
logger.setLevel(logging.ERROR)
file_handler = RotatingFileHandler(
    'logs/api.log', maxBytes=1048576, backupCount=10)
file_handler.setFormatter(logging.Formatter(
    '[%(asctime)s] %(levelname)s: %(message)s - [%(pathname)s:%(lineno)s]'))
logger.addHandler(file_handler)


# To log request only after every request
request_logger = logging.getLogger('request_logger')
request_logger.setLevel(logging.INFO)
request_handler = RotatingFileHandler(
    'logs/request.log', maxBytes=1048576, backupCount=5)
request_handler.setFormatter(logging.Formatter('[%(asctime)s] - %(message)s'))
request_logger.addHandler(request_handler)
