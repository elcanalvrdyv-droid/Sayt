from flask import Flask, render_template, send_from_directory
from flask_socketio import SocketIO, emit
import os

app = Flask(__name__, static_folder='.', template_folder='.')
app.config['SECRET_KEY'] = 'sevgili_secret_key_123!'

# CORS və WebSocket konfiqurasiyası
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='gevent')

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

# Video İdarəetmə Hadisəsi (Play, Pause, Seek)
@socketio.on('video_control')
def handle_video_control(data):
    # Gələn əmri digər qoşulan istifadəçiyə ötürür
    emit('video_control', data, broadcast=True, include_self=False)

# Video Dəyişdirilməsi Hadisəsi
@socketio.on('change_video')
def handle_change_video(data):
    emit('change_video', data, broadcast=True)

# Çat Mesajı Hadisəsi
@socketio.on('send_message')
def handle_message(data):
    from flask import request
    emit('receive_message', {
        'text': data['text'],
        'senderId': request.sid
    }, broadcast=True)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    socketio.run(app, host='0.0.0.0', port=port)