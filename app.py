import logging
from os import getenv

from flask import Flask, request

import db
from api import TgApi
from bot_brains import process_nmessage

app = Flask(__name__)
tg_api = TgApi(getenv('TG_TOKEN'))

# Инициализируем все таблички в бд
db.create_tables()

# Логируем все что у нас есть в gunicorn, чтобы было видно в консоли
if __name__ != '__main__':
    gunicorn_logger = logging.getLogger('gunicorn.error')
    app.logger.handlers = gunicorn_logger.handlers
    # Учитываем уровень логов самого gunicorn
    app.logger.setLevel(gunicorn_logger.level)


@app.route('/')
def hello_world():
    return 'Hello World!'


# Обрабатываем телеграмовы сообщения
@app.route('/telegram-handler', methods=['POST'])
def telegram():
    json = request.get_json()

    if json.get('message'):
        message = tg_api.get_nmessage(json['message'])
        app.logger.info('Telegram message: {}'.format(message.__repr__()))
        process_nmessage(message)

    return 'Ok'


if __name__ == '__main__':
    app.run()
