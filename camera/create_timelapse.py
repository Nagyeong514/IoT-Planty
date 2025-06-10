# camera/create_timelapse.py

import subprocess

# 이미지 폴더 및 출력 영상 경로
image_dir = "/home/annagyeong/Projects/smart_pot_project/timelapse"
output_video = "/home/annagyeong/Projects/smart_pot_project/static/timelapse.mp4"

# ffmpeg 실행 → 이미지들을 영상으로 변환
subprocess.run([
    "ffmpeg",
    "-framerate", "10",
    "-pattern_type", "glob",
    "-i", f"{image_dir}/img_*.jpg",
    "-c:v", "libx264",
    "-pix_fmt", "yuv420p",
    "-r", "30",
    "-y", output_video
])

print(f"🎞️ Timelapse created: {output_video}")
