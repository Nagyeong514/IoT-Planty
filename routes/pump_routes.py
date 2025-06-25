# routes/pump_routes.py
from flask import Blueprint, jsonify
from actuators.pump_relay import pump_on
from scheduler.auto_watering import auto_water_if_needed
from services.save_watering_log import save_watering_log
from flask import request
from db import get_connection
from datetime import datetime, timedelta


pump_bp = Blueprint('pump', __name__)

@pump_bp.route('/api/pump', methods=['POST'])
def trigger_pump():
    pump_on()
    save_watering_log(method='manual')
    return jsonify({"status": "success", "message": "Pump activated"})

@pump_bp.route('/api/pump/auto', methods=["POST"])
def auto_water():
    result = auto_water_if_needed()
    return jsonify(result)


# ✅ 급수 기록 조회 API (그래프용)
@pump_bp.route('/api/pump/logs', methods=['GET'])
def get_watering_logs():
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
        SELECT timestamp, method
        FROM watering_log
        WHERE timestamp >= %s
        ORDER BY timestamp ASC
    """, (since,))
    rows = cursor.fetchall()

    cursor.close()
    conn.close()

    return jsonify(rows)
