# routes/sensor_routes.py
from flask import Blueprint, jsonify
from sensors.soil_sensor import read_soil_moisture
from sensors.dht_sensor import read_temperature_humidity
from sensors.light_sensor import read_light
from scheduler.auto_light import led_mode 
from flask import request  
from db import get_connection  
from datetime import datetime, timedelta



sensor_bp = Blueprint('sensor', __name__)

@sensor_bp.route('/api/soil')
def get_soil_status():
    is_dry = read_soil_moisture()
    return jsonify({
        "status": "dry" if is_dry else "wet",
        "value": int(is_dry)
    })

@sensor_bp.route('/api/dht')
def get_dht():
    data = read_temperature_humidity()
    return jsonify(data)

# ✅ 통합 센서 상태 API
@sensor_bp.route('/api/sensor/current', methods=['GET'])
def get_sensor_data():
    soil_dry = read_soil_moisture()
    dht = read_temperature_humidity()
    light = read_light()  # 0 = dark, 1 = bright

    return jsonify({
        "temperature": dht.get("temperature"),
        "humidity": dht.get("humidity"),
       "soilMoisture": soil_dry,  # ✅ bool 값 그대로 전달
        "light": "dark" if light == 0 else "bright",
        "led": {
            "mode": led_mode["mode"],
            "state": led_mode["state"]
        }
    })

# ✅ 센서 로그 추이 API 추가
@sensor_bp.route('/api/sensor/logs', methods=['GET'])
def get_sensor_logs():
    range_param = request.args.get('range', '7d')

    now = datetime.now()
    if range_param.endswith('d'):
        days = int(range_param[:-1])
        since = now - timedelta(days=days)
    elif range_param.endswith('h'):
        hours = int(range_param[:-1])
        since = now - timedelta(hours=hours)
    else:
        return jsonify({'error': 'Invalid range format'}), 400

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT timestamp, temperature, humidity, soil_dry
        FROM sensor_log
        WHERE timestamp >= %s
        ORDER BY timestamp ASC
    """, (since,))
    rows = cursor.fetchall()

    cursor.close()
    conn.close()

    return jsonify(rows)


