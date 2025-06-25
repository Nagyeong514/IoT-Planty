# routes/led_routes.py

from flask import Blueprint, request, jsonify
from sensors.light_sensor import read_light
from actuators.led_relay import led_on, led_off
from scheduler.auto_light import led_mode
from services.save_led_log import save_led_log  # ✅ 로그 저장 함수 import

led_bp = Blueprint('led', __name__)

# ✅ 조도 센서 상태 조회
@led_bp.route('/api/light')
def get_light():
    value = read_light()
    return jsonify({
        'light': 'dark' if value == 0 else 'bright',
        'value': int(value)
    })

# ✅ LED 상태 및 모드 변경 API
@led_bp.route('/api/led', methods=['POST'])
def control_led():
    try:
        data = request.get_json()
        action = data.get('action')

        if action == 'on':
            led_mode['mode'] = 'manual'
            led_on()
            led_mode['state'] = 'on'
            save_led_log(mode='manual', state='on')

        elif action == 'off':
            led_mode['mode'] = 'manual'
            led_off()
            led_mode['state'] = 'off'
            save_led_log(mode='manual', state='off')

        elif action == 'auto':
            led_mode['mode'] = 'auto'
            # 자동 모드 전환 시 현재 상태는 유지
            save_led_log(mode='auto', state=led_mode['state'])

        else:
            return jsonify({'status': 'error', 'message': 'Invalid action'}), 400

        return jsonify({
            'status': 'ok',
            'mode': led_mode['mode'],
            'state': led_mode['state']
        })

    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

# ✅ 현재 LED 상태 및 모드 조회
@led_bp.route('/api/led/status')
def get_led_status():
    return jsonify({
        'mode': led_mode['mode'],
        'state': led_mode['state']
    })
