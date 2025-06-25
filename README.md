# 🌿 스마트 화분 IoT 프로젝트

센서, 펌프, 카메라, GPT 챗봇을 통합한 라즈베리파이 기반 반려식물 IoT 시스템입니다.



## 📂 브랜치 구조 안내

이 프로젝트는 기능별로 브랜치를 나누어 관리합니다:

- `main`: 전체 프로젝트의 기본 브랜치 (백엔드 + 하드웨어 제어 포함)
- `frontend`: React 기반 대시보드 UI 전용 브랜치
- `modeling`: 스마트 화분을 3D 프린터로 출력하기 위한 모델링 파일 전용 브랜치

각 브랜치는 목적에 따라 코드가 분리되어 있으며, `main` 브랜치 기준으로 병합되지 않은 상태로 개별 유지됩니다.

---

## 🚀 주요 기능

- 온도, 습도, 토양 수분, 조도 실시간 측정
- 기준 이하 시 자동 급수/LED 제어 (릴레이 제어)
- 웹 대시보드에서 수동 급수/LED 제어 가능
- 실시간 스트리밍 + 타임랩스 영상 제공
- OpenAI 기반 식물 챗봇 (감정 표현 포함)

---

## 🛠️ 기술 스택

| 구분       | 사용 기술 |
|------------|-----------|
| 백엔드     | Python, Flask, MySQL, OpenCV |
| 프론트엔드 | React, Chart.js, CSS          |
| 하드웨어   | Raspberry Pi, DHT11, 토양센서, 릴레이, 카메라 |
| 외부 API   | OpenAI GPT, Google STT, Google TTS, Porcupine |

---

## 🔗 연결 방식

- React 앱은 `npm run build` 후 `/static/` 폴더에 복사
- Flask는 정적 웹 + `/api/...` 라우터 제공
- `/video_feed`로 실시간 영상 스트리밍
- 모든 센서/제어는 Flask API 경유

---

## 📡 주요 API

| 메서드 | 경로                  | 기능 설명               |
|--------|-----------------------|------------------------|
| `GET`  | `/api/sensor/latest` | 최신 센서값 반환       |
| `POST` | `/api/pump`          | 수동 급수 (3초 펌프 작동) |
| `GET`  | `/video_feed`        | 실시간 MJPEG 스트리밍 |
| `POST` | `/chatbot`           | GPT 챗봇 응답 반환     |
| `GET`  | `/api/mood/latest`   | 현재 감정 상태 및 이유 |

---

## ⚙️ 설치 및 실행

```bash
# 백엔드 설치
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# React 프론트 빌드
cd client
npm install
npm run build
cp -r build/* ../static/
```

---

## 📌 주의사항

- 토양센서 전원: 반드시 **3.3V** 사용
- 실시간 스트리밍은 MJPEG → **CPU 부하 주의**
- `.env` 또는 환경변수로 Google/OpenAI/picovoice API 키 필요

---

## 🎥 시연 자료

- 발표자료(시연영상 포함): [Canva 링크](https://www.canva.com/design/DAGqYxE9_vU/lQ9is7Os6dEzJnHm8OGzvw/edit)
  
---

## 🧠 주요 외부 API

| 이름             | 기능 설명                    |
|------------------|-----------------------------|
| 🧠 **OpenAI GPT** | 질문 이해 + 답변 생성         |
| 🗣️ **Google STT** | 음성 인식 (STT)             |
| 🔊 **Google TTS** | 챗봇 답변을 음성으로 재생    |
| 🪄 **Porcupine**  | "플랜티야" 웨이크워드 감지   |

---

## ✅ 완료된 기능 체크리스트

- [x] 센서값 수집 및 표시
- [x] 자동 급수 로직
- [x] 수동 급수 버튼 작동
- [x] 실시간 영상 확인 가능
- [x] GPT 챗봇 응답 정상
- [x] 표정 변화 및 감정 로직 연동

---

## 📄 라이선스

MIT License
