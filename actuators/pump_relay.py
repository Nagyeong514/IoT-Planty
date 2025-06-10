# actuators/pump_relay.py

from gpiozero import OutputDevice
import time

# 릴레이가 연결된 GPIO 핀 번호
RELAY_PIN = 27

# 릴레이 객체 생성 (초기 상태: 꺼짐)
relay = OutputDevice(RELAY_PIN, active_high=True, initial_value=False)

def pump_on(duration=1):
    relay.on()  # 릴레이 ON → 펌프 작동
    print("🚿 펌프 작동 시작")
    time.sleep(duration)
    relay.off()  # 릴레이 OFF → 펌프 정지
    print("✅ 펌프 작동 완료")

if __name__ == "__main__":
    try:
        pump_on()
    except KeyboardInterrupt:
        print("\n⏹ 작동 중단됨")
