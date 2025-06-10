# actuators/led_relay.py

from gpiozero import OutputDevice

# ✅ active_high=True → GPIO HIGH = 릴레이 ON
relay = OutputDevice(23, active_high=True, initial_value=False)

def led_on():
    print("LED ON 실행됨")
    relay.on()

def led_off():
    print("LED OFF 실행됨")
    relay.off()
