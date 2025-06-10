## camera/timelapse_capture.py

import os
import datetime
import subprocess

# 저장 경로
save_dir = "/home/annagyeong/Projects/smart_pot_project/timelapse"
os.makedirs(save_dir, exist_ok=True)

# 파일명 생성 (img_YYYYMMDD_HHMM.jpg)
timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M")
filename = f"img_{timestamp}.jpg"
filepath = os.path.join(save_dir, filename)

# 촬영 실행
subprocess.run(["libcamera-jpeg", "-o", filepath])
print(f"📸 Captured: {filepath}")
