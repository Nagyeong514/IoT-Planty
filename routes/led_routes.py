from flask import Blueprint, request, jsonify
from sensors.light_sensor import read_light
from actuators.led_relay import led_on, led_off
from scheduler.auto_light import led_mode

led_bp = Blueprint('led', __name__)

@led_bp.route('/api/light')
def get_light():
    value = read_light()
    return jsonify({
        'light': 'dark' if value == 0 else 'bright',
        'value': int(value)
    })

@led_bp.route('/api/led', methods=['POST'])
def control_led():
    try:
        data = request.get_json()
        action = data.get('action')

        if action == 'on':
            led_mode['mode'] = 'manual'
            led_on()
            led_mode['state'] = 'on'
        elif action == 'off':
            led_mode['mode'] = 'manual'
            led_off()
            led_mode['state'] = 'off'
        elif action == 'auto':
            led_mode['mode'] = 'auto'
        else:
            return jsonify({'status': 'error', 'message': 'Invalid action'}), 400

        return jsonify({
            'status': 'ok',
            'mode': led_mode['mode'],
            'state': led_mode['state']
        })

    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

# ✅ 추가: LED 상태 주기 조회용
@led_bp.route('/api/led/status')
def get_led_status():
    return jsonify({
        'mode': led_mode['mode'],
        'state': led_mode['state']
    })
