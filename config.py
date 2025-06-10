# config.py

# GPIO 핀 설정
SOIL_SENSOR_PIN = 17    # 토양 습도 센서 (GPIO17)
RELAY_PIN = 27          # 릴레이 제어 핀 (GPIO27)
DHT_PIN = 4             # DHT11 온습도 센서 (GPIO4)

# 자동 급수 쿨타임 (초)
COOL_TIME = 600         # 10분




DB_CONFIG = {
    'host': 'localhost',
    'user': 'plantbot',
    'password': 'YourPassword123!',
    'database': 'smart_pot'
}
