from flask import Flask, jsonify
import requests
from flask_cors import CORS
app = Flask(__name__)
CORS(app)
# Замените на токен своего Telegram-бота
BOT_TOKEN = '7687972992:AAGJNdajKIHbcYNGPm7fPX1aWKYrpAAILlk'
TELEGRAM_API_URL = f'https://api.telegram.org/bot{BOT_TOKEN}/getUpdates'


@app.route('/getUpdates', methods=['GET'])
def get_updates():
    try:
        response = requests.get(TELEGRAM_API_URL)
        if response.status_code == 200:
            return jsonify(response.json())
        else:
            return jsonify({'error': 'Telegram API error'}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
