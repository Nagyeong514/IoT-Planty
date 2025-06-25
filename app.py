# app.py

from flask import Flask, send_from_directory
import os
import time
import threading
from flask_cors import CORS
app = Flask(__name__)
CORS(app)


from sensors.soil_sensor import read_soil_moisture
from sensors.dht_sensor import read_temperature_humidity
from actuators.pump_relay import pump_on
from scheduler.auto_watering import auto_water_if_needed
from routes.led_routes import led_bp
from scheduler.auto_light import auto_light_loop
from routes.chatbot import chat_bp
from routes.sensor_routes import sensor_bp
from routes.pump_routes import pump_bp
from routes.log_summary_routes import log_bp
from routes.mood_routes import mood_bp
from ai.planty_voice_agent import PlantyVoiceAgent
from routes.voicechat_route import voice_bp
from routes.camera_stream import camera_bp
from flask import send_from_directory




# ✅ DB 저장 함수 import
from services.save_sensor_data import save_sensor_data
from services.save_watering_log import save_watering_log
from scheduler.sensor_scheduler import sensor_logging_loop




app = Flask(__name__)
app.register_blueprint(led_bp)
app.register_blueprint(chat_bp)
app.register_blueprint(sensor_bp)
app.register_blueprint(pump_bp)
app.register_blueprint(log_bp)
app.register_blueprint(mood_bp)
app.register_blueprint(voice_bp)
app.register_blueprint(camera_bp)


threading.Thread(target=PlantyVoiceAgent().run, daemon=True).start()


# 이모지
@app.route('/face/<path:filename>')
def serve_face(filename):
    return send_from_directory('static/face', filename)

@app.route('/icon/<path:filename>')
def serve_icon(filename):
    return send_from_directory('static/icon', filename)

# React 정적 웹페이지 서빙
@app.route('/')
def index():
    return send_from_directory('static', 'index.html')

# React 빌드된 정적 파일(js, css 등) 처리
@app.route('/static/js/<path:filename>')
def serve_js(filename):
    return send_from_directory('static/static/js', filename)

@app.route('/static/css/<path:filename>')
def serve_css(filename):
    return send_from_directory('static/static/css', filename)

@app.route('/static/timelapse.mp4')
def serve_timelapse():
    return send_from_directory('static', 'timelapse.mp4')




# 🔄 자동 급수 백그라운드 루프
def auto_watering_loop():
    print("✅ 백그라운드 자동 급수 시작 (60초 간격)")
    while True:
        result = auto_water_if_needed()
        print(f"[AUTO] {result}")
        time.sleep(60)

if __name__ == '__main__':
    threading.Thread(target=auto_watering_loop, daemon=True).start()
    threading.Thread(target=sensor_logging_loop, daemon=True).start()
    threading.Thread(target=auto_light_loop, daemon=True).start()
    app.run(host='0.0.0.0', port=5000)
