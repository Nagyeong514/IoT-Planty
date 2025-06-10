## sensors/soil_sensor.py

from gpiozero import DigitalInputDevice
import time

# GPIO17 (핀 11)
sensor = DigitalInputDevice(17)

def read_soil_moisture():
    # True = 건조함, False = 습함
    return True if sensor.value == 1 else False

if __name__ == "__main__":
    try:
        print("💧 Soil Moisture Monitoring Start (Ctrl+C to exit)")
        while True:
            is_dry = read_soil_moisture()
            if is_dry:
                print("Dry 🌱")
            else:
                print("Wet 💦")
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n✅ 종료 중... 센서 정지")
