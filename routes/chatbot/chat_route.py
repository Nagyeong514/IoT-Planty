# routes/chatbot/chat_route.py

from flask import Blueprint, request, jsonify
from db import get_connection
from openai import OpenAI
from dotenv import load_dotenv
from .intent import get_intent
from .response_prompt import build_prompt
from .log import maybe_save_mood_log
import os

load_dotenv()

# print("🔍 OPENAI_API_KEY =", os.getenv("OPENAI_API_KEY"))  // 아니 왜 또 안돼 다시 발급해라

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

chat_bp = Blueprint('chat', __name__)

@chat_bp.route('/api/chat', methods=['POST'])
def chat():
    user_msg = request.json.get('message')
    intent = get_intent(user_msg)

     # ✅ 추천 질문일 경우 실제 intent로 매핑
    if intent == "RECOMMENDED_QUESTION":
        if "상태" in user_msg:
            intent = "CURRENT_STATUS"
        elif "기분" in user_msg:
            intent = "EMOTIONAL_CHECK"
        elif "물" in user_msg or "언제" in user_msg:
            intent = "LAST_WATERED"
    
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    prompt, log_data = build_prompt(intent, user_msg, cursor)
    maybe_save_mood_log(log_data)  # log_data가 None이면 저장 안 함

    cursor.close()
    conn.close()

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )
    reply = response.choices[0].message.content
    return jsonify({ "reply": reply, "face": log_data["face"]   })

# ✅ 공용 GPT 응답 생성 함수
def get_gpt_reply(prompt: str) -> str:
    """
    GPT 프롬프트를 기반으로 응답 텍스트 생성
    """
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content