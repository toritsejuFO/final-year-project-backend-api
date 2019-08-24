import os
import logging
from logging.handlers import RotatingFileHandler

if not os.path.exists('logs'):
    os.mkdir('logs')


file_handler = RotatingFileHandler(
    'logs/api.log', maxBytes=1048576, backupCount=10)
file_handler.setLevel(logging.ERROR)
file_handler.setFormatter(logging.Formatter(
    '[%(asctime)s] %(levelname)s: %(message)s - [%(pathname)s:%(lineno)s]'))

# To log request only after every request
request_logger = logging.getLogger('request_logger')
request_handler = RotatingFileHandler(
    'logs/request.log', maxBytes=1048576, backupCount=5)
request_handler.setLevel(logging.INFO)
request_handler.setFormatter(logging.Formatter('[%(asctime)s] - %(message)s'))
request_logger.addHandler(request_handler)
