import requests
from abc import ABCMeta, abstractmethod
from utils import LoggingMixin


class ABC_SMSHandler(metaclass=ABCMeta):
    """
    Абстрактный базовый класс для реализации смс хэндлеров
    """
    logger = LoggingMixin()

    @property
    @abstractmethod
    def API_URL(self):
        """
        URL api гейта.
        Должен быть переопределено в каждом дочернем классе.
        """
        pass

    def __init__(self, login, password):
        self.login = login
        self.password = password

    @abstractmethod
    def send(self, data):
        """
        Метод отправки sms сообщений посредством api гейта.
        Должен быть расширен (переопределен и вызван) в каждом дочернем классе.
        """
        response = requests.post(self.API_URL, data=data, json=True)

        if response.status_code == 401:
            # Что-то делать, если гейт вернул 401 Unauthorized
            raise NotImplementedError

        response_data = response.json()

        # Логгирование отправки sms сообщений.
        status = response_data.get('status')

        if status is None:
            raise ValueError('Could not find "status" value')
        elif status == 'ok':
            self.logger.access(response_data)
        elif status == 'error':
            self.logger.error(response_data)

        return response_data


class SMSRU_SMSHandler(ABC_SMSHandler):
    """
    SMSRU
    http://sms.ru/
    """
    API_URL = 'http://smsc.ru/some­api/message/'

    def send(self, to, text):
        data = {
            'login': self.login,
            'password': self.password,
            'to': to,
            'text': text
        }
        return super(SMSRU_SMSHandler, self).send(data)


class SMSTRAFFIC_SMSHandler(ABC_SMSHandler):
    """
    SMS Traffic
    http://smstraffic.ru/
    """
    API_URL = 'http://smstraffic.ru/super­api/message/'

    def __init__(self, token, password, something_else):
        self.token = token
        self.password = password
        self.something_else = something_else

    def send(self, to, text):
        data = {
            'token': self.token,
            'password': self.password,
            'something_else': self.something_else,
            'to': to,
            'text': text
        }
        return super(SMSTRAFFIC_SMSHandler, self).send(data)


class KIDSTIC_SMSHandler(ABC_SMSHandler):
    """
    Тестовый sms гейт.
    """
    API_URL = 'https://www.kidstic.ru/api.php'

    def send(self, to, text):
        data = {
            'login': self.login,
            'password': self.password,
            'to': to,
            'text': text
        }
        return super(KIDSTIC_SMSHandler, self).send(data)
