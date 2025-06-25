from datetime import datetime
from services.mood_evaluator import evaluate_mood
from db import get_connection

# 💡 LED 상태 가져오기 함수

def get_led_state():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM led_log ORDER BY id DESC LIMIT 1")
    row = cursor.fetchone()
    cursor.close()
    conn.close()
    return row['state'] if row else 'off'

# ✅ 센서 데이터 기반 정보 구성 함수

def get_latest_sensor_data(cursor):
    cursor.execute("SELECT * FROM sensor_log ORDER BY timestamp DESC LIMIT 1")
    row = cursor.fetchone()
    return {
        "temperature": row['temperature'],
        "humidity": row['humidity'],
        "soil_dry": row['soil_dry'],
        "light": row.get('light') or 'unknown'
    }

def get_last_watering(cursor):
    cursor.execute("SELECT * FROM watering_log ORDER BY timestamp DESC LIMIT 1")
    row = cursor.fetchone()
    if row:
        return row['timestamp'].strftime('%Y년 %m월 %d일 %H시 %M분'), row['method']
    else:
        return "기록 없음", "unknown"

# ✅ 질문 intent와 데이터에 따라 프롬프트 생성

def build_prompt(intent, user_msg, cursor):
    today_str = datetime.now().strftime('%Y년 %m월 %d일')
    sensor = get_latest_sensor_data(cursor)
    led_state = get_led_state()
    mood = evaluate_mood(sensor['temperature'], sensor['humidity'], sensor['soil_dry'], sensor['light'], led_state)

    mood_type = mood["mood_type"]
    face = mood["face"]
    reason = mood["reason"]
    text = mood["text"]

    mood_summary = f"""
- 플랜티 기분: {mood_type}
- 이유: {reason}
""".strip()

    common_context = f"""
오늘 날짜: {today_str}
- 온도: {sensor['temperature']}°C
- 습도: {sensor['humidity']}%
- 토양 상태: {'건조함' if sensor['soil_dry'] else '촉촉함'}
- 주변 밝기: {sensor['light']}
{mood_summary}
""".strip()

    # intent별 프롬프트 정의

    if intent == 'CURRENT_STATUS':
        prompt = f"""
{user_msg}

플랜티는 감정을 느끼는 식물이에요. 아래 정보를 바탕으로 지금 상태를 사용자에게 부드럽고 감성적으로 설명해주세요.

📌 요청사항:
- 온도, 습도, 토양 상태, 밝기 등을 1~2문장으로 설명
- 플랜티의 기분도 함께 표현
- 말투는 따뜻하고 정중하게, 식물이 직접 말하듯
- 이모티콘 사용 금지
- 마지막 문장은 꼭 "혹시 또 궁금한 게 있나요? "

📦 참고 정보:
{common_context}
""".strip()


    elif intent == 'LAST_WATERED':
        time_str, method = get_last_watering(cursor)
        prompt = f"""
{user_msg}

사용자에게 마지막으로 물 준 시점과 방식만 간단히 알려주세요.

📌 요청사항:
- 너무 감성적으로 쓰지 말고 정중한 말투로 정보만 안내
- 센서 수치나 기분은 말하지 않기
- 이모티콘 사용 금지
- 마지막 문장은 "혹시 또 궁금한 게 있나요? "

🕒 최근 급수 정보:
- 시간: {time_str}
- 방식: {'수동' if method == 'manual' else '자동'}
""".strip()


    elif intent == 'EMOTIONAL_CHECK':
        prompt = f"""
{user_msg}

플랜티는 감정을 느껴요. 아래 데이터를 참고해서 지금 어떤 기분인지 짧고 따뜻하게 말해주세요.

📌 요청사항:
- 기분 요약 + 이유 (예: 온도가 너무 높아서 덥다고 느껴요)
- 문장은 2줄 이내로
- 말투는 부드럽고 감성적인 느낌
- 이모티콘 사용 금지
- 마지막 문장은 꼭 "혹시 또 궁금한 게 있나요? "

📦 참고 정보:
{common_context}
""".strip()


    

    else:  # 기본 fallback
        prompt = f"""
{user_msg}

플랜티라는 감성적인 식물 캐릭터가 사용자 질문에 답변하되, 자신의 기분도 자연스럽게 포함해주세요.

📌 요청사항:
- 자유로운 방식으로 2~3문장 응답
- 현재 기분({mood_type})을 자연스럽게 반영
- 이모티콘 사용 금지
- 마지막 문장은 "혹시 또 궁금한 게 있나요? "

📦 참고 정보:
{common_context}
""".strip()

    return prompt, {
        "mood_type": mood_type,
        "face": face,
        "reason": reason,
        "temperature": sensor['temperature'],
        "humidity": sensor['humidity'],
        "soil_dry": sensor['soil_dry'],
        "light": sensor['light'],
        "text": text
    }
