## scheduler/sensor_scheduler.py

import time
from sensors.soil_sensor import read_soil_moisture
from sensors.dht_sensor import read_temperature_humidity
from services.save_sensor_data import save_sensor_data

def sensor_logging_loop():
    print("🕒 센서 자동 기록 시작 (30분 간격)")
    while True:
        soil = read_soil_moisture()
        dht = read_temperature_humidity()
        save_sensor_data(
            temperature=dht.get("temperature"),
            humidity=dht.get("humidity"),
            soil_dry=soil
        )
        print("✅ 센서 값 저장 완료")
        time.sleep(1800)  # 30분 = 1800초
