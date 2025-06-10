# auto_watering_runner.py - test

import time
from scheduler.auto_watering import auto_water_if_needed

if __name__ == "__main__":
    print("🔄 자동 급수 루프 시작 (1분 간격)")
    while True:
        result = auto_water_if_needed()
        print(f"[AUTO] {result}")
        time.sleep(60)  # 60초마다 검사
