# routes/chat_route.py

from dotenv import load_dotenv
import os
from flask import Blueprint, request, jsonify
from db import get_connection
from openai import OpenAI
import datetime

# 🔑 .env에서 API 키 불러오기
load_dotenv()
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

chat_bp = Blueprint('chat', __name__)

# GPT에게 질문 의도(intent) 추출
def get_intent(message):
    prompt = f"""
    사용자의 질문에서 의도를 아래 중 하나로 판단해서 해당 이름만 출력해.
    - CURRENT_STATUS: 지금 상태 어때?
    - LAST_WATERED: 최근에 물 준 시간
    - EMOTIONAL_CHECK: 요즘 기분 어때?

    질문: "{message}"
    답변은 반드시 의도 키워드만 출력해.
    """

    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content.strip()

# 챗봇 API 라우트
@chat_bp.route('/api/chat', methods=['POST'])
def chat():
    user_msg = request.json.get('message')
    intent = get_intent(user_msg)

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    if intent == 'CURRENT_STATUS':
        cursor.execute("SELECT * FROM sensor_log ORDER BY timestamp DESC LIMIT 1")
        row = cursor.fetchone()
        data = f"온도 {row['temperature']}°C, 습도 {row['humidity']}%, 토양 상태는 {'건조함' if row['soil_dry'] else '촉촉함'}입니다."
        prompt = f"""
        질문: {user_msg}
        식무리의 현재 상태는 다음과 같아요:
        {data}
        식무리라는 이름의 귀여운 식물이 감성적으로 사용자에게 알려주는 말투로 한국어로 대답해줘.
        줄바꿈과 이모티콘도 자연스럽게 포함해줘.
        """

    elif intent == 'LAST_WATERED':
        cursor.execute("SELECT * FROM watering_log ORDER BY timestamp DESC LIMIT 1")
        row = cursor.fetchone()
        time_str = row['timestamp'].strftime('%Y년 %m월 %d일 %H시 %M분')
        method = "수동으로" if row['method'] == 'manual' else "자동으로"
        prompt = f"""
        질문: {user_msg}
        가장 최근 물 준 기록은 다음과 같아요:
        - 시간: {time_str}
        - 방식: {method}
        이 정보를 바탕으로 식무리가 말하듯이 대답해줘. 귀엽고 따뜻한 말투로.
        """

    elif intent == 'EMOTIONAL_CHECK':
        cursor.execute("SELECT * FROM sensor_log ORDER BY timestamp DESC LIMIT 1")
        row = cursor.fetchone()
        mood = "물을 안 줘서 살짝 목이 말라요... 🥺" if row['soil_dry'] else "토양이 촉촉해서 기분이 좋아요! 🌸"
        prompt = f"""
        질문: {user_msg}
        식무리의 상태 분석 결과:
        {mood}
        이 느낌을 바탕으로 식무리가 감성적으로 대답해줘. 너무 길진 않게, 이모티콘 포함.
        """

    else:
        prompt = f"""
        질문: {user_msg}
        식무리라는 식물 캐릭터가 예의 바르게 응답해줘. 너무 길지 않게.
        """

    cursor.close()
    conn.close()

    # GPT 응답 생성 (최신 방식)
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )
    reply = response.choices[0].message.content
    return jsonify({"reply": reply})
