# routes/log_summary_route.py

from flask import Blueprint, jsonify
from db import get_connection

log_bp = Blueprint('log', __name__)

@log_bp.route('/api/logs/summary')
def get_summary():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    # 1. 센서 평균
    cursor.execute("""
        SELECT 
            ROUND(AVG(temperature), 1) AS avg_temp,
            ROUND(AVG(humidity), 1) AS avg_humi,
            ROUND(SUM(soil_dry) / COUNT(*), 2) AS dry_ratio
        FROM sensor_log
        WHERE timestamp >= NOW() - INTERVAL 1 DAY
    """)
    sensor_data = cursor.fetchone()

    # 2. 조도 비율
    cursor.execute("""
        SELECT 
            COUNT(*) AS total,
            SUM(CASE WHEN light = 'dark' THEN 1 ELSE 0 END) AS dark_count
        FROM sensor_log
        WHERE timestamp >= NOW() - INTERVAL 1 DAY
    """)
    light_row = cursor.fetchone()
    dark_ratio = round(light_row['dark_count'] / light_row['total'], 2) if light_row['total'] else None

    # 3. LED 꺼짐 횟수
    cursor.execute("""
        SELECT COUNT(*) AS off_count
        FROM led_log
        WHERE state = 'off' AND timestamp >= NOW() - INTERVAL 1 DAY
    """)
    led_row = cursor.fetchone()

    cursor.close()
    conn.close()

    return jsonify({
        "temperature_avg": sensor_data['avg_temp'],
        "humidity_avg": sensor_data['avg_humi'],
        "soil_dry_ratio": sensor_data['dry_ratio'],
        "dark_ratio": dark_ratio,
        "led_off_count": led_row['off_count']
    })


# ✅ 1. 마지막 급수 로그
@log_bp.route('/api/logs/last-watering')
def get_last_watering():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT timestamp, method
        FROM watering_log
        ORDER BY timestamp DESC
        LIMIT 1
    """)
    row = cursor.fetchone()
    cursor.close()
    conn.close()

    return jsonify(row if row else {"timestamp": None, "method": None})

# ✅ 2. 마지막 감정 로그
@log_bp.route('/api/logs/mood-reason')
def get_last_mood():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT timestamp, mood_type, face_expression, reason
        FROM mood_log
        ORDER BY timestamp DESC
        LIMIT 1
    """)
    row = cursor.fetchone()
    cursor.close()
    conn.close()

    return jsonify(row if row else {
        "timestamp": None,
        "mood_type": None,
        "face_expression": None,
        "reason": None
    })

