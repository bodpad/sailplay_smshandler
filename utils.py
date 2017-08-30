import logging
from importlib import import_module


def get_handler(handler_name):
    """
    Фабрика, которая возвращает желаемый sms хендлер.
    handler_name - название файла,
    """
    module = import_module("sms_handlers")
    return getattr(module, handler_name)


class LoggingMixin:

    def __init__(self):
        formatter = logging.Formatter('%(asctime)s %(message)s')

        # Access logging
        self.access_logger = logging.getLogger('access')
        handler = logging.FileHandler('logs/access.log')
        self.access_logger.setLevel(logging.INFO)
        handler.setFormatter(formatter)
        self.access_logger.addHandler(handler)

        # Error logging
        self.error_logger = logging.getLogger('error')
        handler = logging.FileHandler('logs/error.log')
        self.error_logger.setLevel(logging.ERROR)
        handler.setFormatter(formatter)
        self.error_logger.addHandler(handler)

    def access(self, response_data):
        self.access_logger.info('status: OK, phone: %s', response_data['phone'])

    def error(self, response_data):
        self.error_logger.error(
            'status: ERROR, phone: %s, error_code: %s, error_msg: %s',
            response_data['phone'],
            response_data['error_code'],
            response_data['error_msg']
        )