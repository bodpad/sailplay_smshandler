from unittest import TestCase
from utils import get_handler


class TestSMSHandler(TestCase):
    def test_kidstic_sms_handler(self):
        sms_handler = get_handler('KIDSTIC_SMSHandler')
        smsapi = sms_handler(login='Korolev', password='qwert12345')
        response = smsapi.send(to='79149009900', text='Ваш код подтверждения - 73584')
        self.assertEqual(response['status'], 'ok')

    # ... другие