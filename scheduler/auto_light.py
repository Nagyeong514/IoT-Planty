# scheduler/auto_light.py 자동 점등 루프 전용

from sensors.light_sensor import read_light
from actuators.led_relay import led_on, led_off
import time

led_mode = {'mode': 'manual', 'state': 'off'}

def auto_light_loop():
    print("✅ 자동 LED 제어 루프 시작 (3초 간격)")
    while True:
        if led_mode['mode'] == 'auto':
            light = read_light()
            if light == 0:  # dark
                led_on()
                led_mode['state'] = 'on'
            else:
                led_off()
                led_mode['state'] = 'off'
        time.sleep(3)

