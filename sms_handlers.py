import requests
import json
from abc import ABCMeta, abstractmethod
from utils import LoggingMixin


class ABC_SMSHandler(metaclass=ABCMeta):
    logger = LoggingMixin()

    @property
    @abstractmethod
    def API_URL(self):
        """
        URL api гейта.
        Должен быть переопределено в каждом дочернем классе.
        """
        pass

    @abstractmethod
    def __init__(self, login, password):
        pass

    @abstractmethod
    def send(self, data):
        """
        Метод отправки sms сообщений посредством api гейта.
        Должен быть расширен (переопределен и вызван) в каждом дочернем классе.
        Возвращает True, если sms гейт вернул статус 'ok' или False, если 'error'
        """
        response = requests.post(self.API_URL, data=data)

        if response.status_code == 401:
            # Что-то делать, если гейт вернул 401 Unauthorized
            raise NotImplementedError

        response_data = json.loads(response.text)

        # Логгирование отправки sms сообщений.
        status = response_data.get('status')

        if status is None:
            raise ValueError('Could not find "status" value')
        elif status == 'ok':
            self.logger.access(response_data)
            return True
        elif status == 'error':
            self.logger.error(response_data)
            return False


class SMSRU_SMSHandler(ABC_SMSHandler):
    """
    SMSRU
    http://sms.ru/
    """
    API_URL = 'http://smsc.ru/some­api/message/'

    def __init__(self, login, password):
        self.login = login
        self.password = password

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

    def __init__(self, token, password):
        self.token = token
        self.password = password

    def send(self, to, text):
        data = {
            'token': self.token,
            'password': self.password,
            'to': to,
            'text': text
        }
        return super(SMSTRAFFIC_SMSHandler, self).send(data)


class KIDSTIC_SMSHandler(ABC_SMSHandler):
    """
    Тестовый sms гейт.
    Разработан мной для тестирования работоспособности кода.
    """
    API_URL = 'https://www.kidstic.ru/api.php'

    def __init__(self, login, password):
        self.login = login
        self.password = password

    def send(self, to, text):
        data = {
            'login': self.login,
            'password': self.password,
            'to': to,
            'text': text
        }
        return super(KIDSTIC_SMSHandler, self).send(data)