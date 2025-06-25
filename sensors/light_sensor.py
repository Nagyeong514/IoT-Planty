## sensors/light_sensor.py

from gpiozero import DigitalInputDevice

light_sensor = DigitalInputDevice(22)

def read_light():
    return 1 - int(light_sensor.value)  # ✅ 반전 적용
