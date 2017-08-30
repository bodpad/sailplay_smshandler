## Развертывание и запуск
    git clone https://github.com/bodpad/sailplay_smshandler.git
    cd sailplay_smshandler
    
    # Устанавливаем виртуальное окружение
    # и все необходимые для работы пакеты
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    
    # Запускаем тест. Результат смотрим в log-файлах
    python3 -m unittest

## Документация
Для добавление нового sms-гейта, необходимо в файла sms_handeler.py добавить соответствующий класс:
    
    class [SMS_GATEWAY_NAME]_SMSHandler(ABC_SMSHandler):
        API_URL = '...'
        
        def send(self, to, text):
            # data - данные необходимых для отправки смс.
            data = {'login': self.login, ...}
            
            # Обязательно вызвать соответствующий метод базового класса
            return super([SMS_GATEWAY_NAME]_SMSHandler, self).send(data)
