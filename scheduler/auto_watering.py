## scheduler/auto_watering.py

import time
import os
from sensors.soil_sensor import read_soil_moisture
from actuators.pump_relay import pump_on
from services.save_watering_log import save_watering_log 

LAST_WATERING_FILE = "logs/last_watering.txt"
COOL_TIME = 600  # 10분

def get_last_watering_time():
    if os.path.exists(LAST_WATERING_FILE):
        with open(LAST_WATERING_FILE, "r") as f:
            return float(f.read().strip())
    return 0.0

def update_last_watering_time():
    with open(LAST_WATERING_FILE, "w") as f:
        f.write(str(time.time()))

def auto_water_if_needed():
    is_dry = read_soil_moisture()
    now = time.time()
    last_time = get_last_watering_time()

    print(f"[DEBUG] is_dry={is_dry}, elapsed={now - last_time:.1f}s")

    if is_dry and (now - last_time > COOL_TIME):
        print("✅ 자동 급수 조건 충족: DRY + 쿨타임 경과")
        pump_on(duration=1)
        update_last_watering_time()
        save_watering_log(method='auto')  # ✅ 여기 추가!
        return {"auto_watered": True, "reason": "dry_and_cooltime_passed"}
    elif is_dry:
        print("⏳ DRY 상태지만 쿨타임 미경과로 대기 중")
        return {"auto_watered": False, "reason": "cooltime_not_passed"}
    else:
        print("💧 토양이 촉촉하므로 급수 불필요")
        return {"auto_watered": False, "reason": "soil_not_dry"}
