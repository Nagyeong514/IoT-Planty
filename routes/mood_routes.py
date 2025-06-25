from flask import Blueprint, jsonify
from db import get_connection

mood_bp = Blueprint('mood', __name__)

@mood_bp.route('/api/mood/latest', methods=['GET'])
def get_latest_mood():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT mood_type, face_expression, reason, timestamp
        FROM mood_log
        ORDER BY timestamp DESC
        LIMIT 1
    """)
    row = cursor.fetchone()
    cursor.close()
    conn.close()

    if row:
        return jsonify({
            "mood": row["mood_type"],
            "face": row["face_expression"],
            "reason": row["reason"],
            "timestamp": row["timestamp"].strftime("%Y-%m-%d %H:%M:%S")
        })
    else:
        return jsonify({
            "error": "No mood data available"
        }), 404


@mood_bp.route('/api/mood/logs', methods=['GET'])
def get_mood_logs():
    from flask import request
    from datetime import datetime, timedelta

    range_param = request.args.get('range', '7d')
    now = datetime.now()
    if range_param.endswith('d'):
        days = int(range_param[:-1])
        since = now - timedelta(days=days)
    else:
        return jsonify({'error': 'Invalid range'}), 400

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT timestamp, mood_type, face_expression, reason
        FROM mood_log
        WHERE timestamp >= %s
        ORDER BY timestamp DESC

    """, (since,))
    rows = cursor.fetchall()
    cursor.close()
    conn.close()

    return jsonify(rows)
