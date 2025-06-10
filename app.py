# app.py

from flask import Flask, render_template, jsonify, url_for, request
import os
import time
import threading

from sensors.soil_sensor import read_soil_moisture
from sensors.dht_sensor import read_temperature_humidity
from actuators.pump_relay import pump_on
from scheduler.auto_watering import auto_water_if_needed
from routes.led_routes import led_bp

from scheduler.auto_light import auto_light_loop
from routes.chat_route import chat_bp


# ✅ DB 저장 함수 import
from services.save_sensor_data import save_sensor_data
from services.save_watering_log import save_watering_log
from scheduler.sensor_scheduler import sensor_logging_loop

app = Flask(__name__)
app.register_blueprint(led_bp)
app.register_blueprint(chat_bp)

@app.route('/')
def index():
    video_path = 'static/timelapse.mp4'
    if not os.path.exists(video_path):
        print("⚠️ 타임랩스 영상이 존재하지 않습니다.")
    timestamp = int(time.time())
    video_url = url_for('static', filename='timelapse.mp4') + f'?v={timestamp}'
    return render_template("index.html", video_url=video_url)

@app.route('/api/soil')
def get_soil_status():
    is_dry = read_soil_moisture()
    return jsonify({
        "status": "dry" if is_dry else "wet",
        "value": int(is_dry)
    })

@app.route('/api/dht')
def get_dht():
    data = read_temperature_humidity()
    return jsonify(data)

@app.route('/api/pump', methods=['POST'])  # ✅ 수동 급수
def trigger_pump():
    pump_on()
    save_watering_log(method='manual')  # ✅ 수동 급수 기록 저장
    return jsonify({"status": "success", "message": "Pump activated"})

@app.route('/api/pump/auto', methods=["POST"])
def auto_water():
    result = auto_water_if_needed()
    return jsonify(result)

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
