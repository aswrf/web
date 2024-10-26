from flask import Flask, render_template, request, jsonify
import requests
from datetime import datetime
import pytz

app = Flask(__name__)

# Thay YOUR_BOT_TOKEN bằng token của bot Telegram của bạn
TELEGRAM_TOKEN = '7980399039:AAHovYsLhT6P_9bfoDjSwLB72KivKm45zfk'
# Thay YOUR_CHAT_ID bằng chat ID của nhóm/kênh Telegram
TELEGRAM_CHAT_ID = '-1002426266844'

def send_to_telegram(message):
    url = f'https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage'
    data = {
        'chat_id': TELEGRAM_CHAT_ID,
        'text': message,
        'parse_mode': 'HTML'
    }
    try:
        response = requests.post(url, data=data)
        return response.json()
    except Exception as e:
        print(f"Error sending to Telegram: {e}")
        return None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/collect', methods=['POST'])
def collect_data():
    data = request.json
    
    # Chuyển đổi thời gian sang múi giờ GMT+7
    vietnam_tz = pytz.timezone('Asia/Ho_Chi_Minh')
    current_time = datetime.now(vietnam_tz).strftime('%Y-%m-%d %H:%M:%S')
    
    # Tạo tin nhắn cho Telegram
    message = (
        f"🔔 <b>Có người truy cập mới!</b>\n\n"
        f"📱 <b>Thiết bị:</b>\n{data['device']}\n\n"
        f"🌐 <b>Địa chỉ IP:</b>\n{data['ip']}\n\n"
        f"⏰ <b>Thời gian:</b>\n{current_time}"
    )
    
    # Gửi thông báo đến Telegram
    send_to_telegram(message)
    
    return jsonify({"status": "success"})

if __name__ == '__main__':
    app.run(debug=True)
