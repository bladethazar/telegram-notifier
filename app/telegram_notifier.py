import os
from metrics_collector import metrics_collector
from flask import Flask, request, jsonify, make_response, url_for
from dotenv import load_dotenv
from datetime import datetime
import sys
import pytz
import requests
import logging

local_timezone = pytz.timezone('Europe/Berlin')
logging.basicConfig(level=logging.INFO, stream=sys.stdout,
                    format='[%(asctime)s.%(msecs)03d] [%(levelname)s]: %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')
logging.Formatter.converter = lambda *args: datetime.now(local_timezone).timetuple()

# Load environment variables
load_dotenv()

app = Flask(__name__)


class TelegramNotifier:
    def __init__(self):
        self.telegram_bot_channel_url = os.getenv('TELEGRAM_BOT_CHANNEL_URL')
        self.telegram_chat_id = os.getenv('TELEGRAM_CHAT_ID')

    def get_chat_id(self):
        response = requests.get(f"{self.telegram_bot_channel_url}/getUpdates")
        data = response.json()
        try:
            if data["ok"]:
                if data["result"]:
                    chat_id = data["result"][0]["message"]["chat"]["id"]
                    return chat_id
        except Exception as e:
            metrics_collector.increment_error_count()
            return {"Error": str(e), "status_code": 500}

    @staticmethod
    @app.route('/send_message', methods=['POST'])
    def send_message():
        try:
            payload = request.json
            if 'message' in payload:
                params = {'chat_id': TelegramNotifier().telegram_chat_id, 'text': payload['message']}
                response = requests.post(f"{TelegramNotifier().telegram_bot_channel_url}/sendMessage", json=params)
                response.raise_for_status()
                app.logger.info(f"Sent message to Telegram-Bot URL: [{TelegramNotifier().telegram_bot_channel_url}] successful.")
                # Increment metrics
                metrics_collector.increment_messages_sent()
                return jsonify(
                    {'message': 'Message sent successfully to Telegram Bot-Channel [rpi_foxhole.notifier]'}), 200
            else:
                return jsonify({'error': 'Invalid payload. Required key: "message"'}), 400
        except Exception as e:
            app.logger.error(f'Telegram message sending failed: {str(e)}')
            return jsonify({'error': 'Internal Server Error'}), 500

    @staticmethod
    @app.route('/send_photo', methods=['POST'])
    def send_photo():
        try:
            image = request.files['photo']
            if image:
                # Send the photo via Telegram API
                files = {'photo': image}
                data = {'chat_id': TelegramNotifier().telegram_chat_id, 'caption': request.form.get('caption', '')}
                response = requests.post(f"{TelegramNotifier().telegram_bot_channel_url}/sendPhoto", data=data, files=files)

                # Check if the request was successful
                if response.status_code == 200:
                    app.logger.info(f"Sent photo to Telegram-Bot URL: [{TelegramNotifier().telegram_bot_channel_url}] successful.")
                    # Increment metrics
                    metrics_collector.increment_photos_sent()
                    return jsonify(
                        {'message': 'Photo sent successfully to Telegram Bot-Channel [rpi_foxhole.notifier]'}), 200
                else:
                    app.logger.error(f"Telegram photo sending failed: {response.json()}")
                    return jsonify({'error': 'Failed to send photo to Telegram'}), response.status_code
            else:
                return jsonify({'error': 'Invalid payload. Required key: "photo"'}), 400
        except Exception as e:
            metrics_collector.increment_error_count()
            app.logger.error(f'Telegram photo sending failed: {str(e)}')
            return jsonify({'error': 'Internal Server Error'}), 400

    @staticmethod
    @app.route('/metrics', methods=['GET'])
    def get_metrics():
        metrics_response = metrics_collector.get_metrics()
        response = make_response(metrics_response)
        response.headers['Content-Type'] = 'text/plain'
        response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
        response.headers['Pragma'] = 'no-cache'
        response.headers['Expires'] = '0'
        response.headers['Link'] = '<{0}>; rel="icon"'.format(url_for('static', filename='favicon.ico'))
        return response


def run_telegram_notifier():
    TelegramNotifier()
    app.run(host='0.0.0.0', port=5000)


if __name__ == "__main__":
    run_telegram_notifier()
