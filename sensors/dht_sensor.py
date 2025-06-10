## sensors/dht_sensor.py

import board
import adafruit_dht

# DHT11 센서 (GPIO4 = board.D4)
dhtDevice = adafruit_dht.DHT11(board.D4)

def read_temperature_humidity():
    try:
        temperature = dhtDevice.temperature
        humidity = dhtDevice.humidity
        return {
            "temperature": temperature,
            "humidity": humidity
        }
    except Exception as e:
        return {
            "temperature": None,
            "humidity": None,
            "error": str(e)
        }
