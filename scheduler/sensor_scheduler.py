import time
from sensors.soil_sensor import read_soil_moisture
from sensors.dht_sensor import read_temperature_humidity
from sensors.light_sensor import read_light
from services.save_sensor_data import save_sensor_data
from services.mood_evaluator import evaluate_mood          # ✅ 표정 평가 함수 import
from services.save_mood_log import save_mood_log           # ✅ 감정 로그 저장
from scheduler.auto_light import led_mode                  # ✅ 현재 LED 상태 확인

def sensor_logging_loop():
    print("🕒 센서 자동 기록 시작 (30분 간격)")
    while True:
        # 센서값 읽기
        soil = read_soil_moisture()
        dht = read_temperature_humidity()
        light = read_light()
        light_str = 'dark' if light == 0 else 'bright'

        # 센서 데이터 저장
        save_sensor_data(
            temperature=dht.get("temperature"),
            humidity=dht.get("humidity"),
            soil_dry=soil,
            light=light_str
        )
        print("✅ 센서 값 저장 완료")

       # ✅ dict로 반환되므로 dict 그대로 받기
        mood = evaluate_mood(
            temperature=dht.get("temperature"),
            humidity=dht.get("humidity"),
            soil_dry=soil,
            light=light_str,
            led_state=led_mode['state']
        )

        save_mood_log(
            mood["mood_type"],
            mood["face"],
            mood["reason"],
            temperature=dht.get("temperature"),
            humidity=dht.get("humidity"),
            soil_dry=soil,
            light=light_str
        )
        print(f"📝 표정 저장됨 → {mood['mood_type']} ({mood['face']})")


        # 30분 대기
        time.sleep(1800)
