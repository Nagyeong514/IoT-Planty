from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def get_intent(message):
    # ✅ 추천 질문 직접 처리
    msg = message.strip()
    if msg in ["지금 상태 어때?", "지금 화분 상태 어때?"]:
        return "CURRENT_STATUS"
    elif msg in ["오늘 기분은 어때?", "지금 기분은 어때?"]:
        return "EMOTIONAL_CHECK"
    elif "물" in msg and "언제" in msg:
        return "LAST_WATERED"

    # ✅ GPT에게 묻기 (그 외의 경우만)
    messages = [
        {
            "role": "system",
            "content": """
너는 스마트 화분 시스템의 **질문 분류기**야.

아래 의도 중 사용자의 질문에 가장 잘 맞는 것 **하나만** 판단해서 **해당 키워드만 한 줄로 출력해**.
절대 문장 쓰지 마. 키워드 외 다른 글자 있으면 오류로 간주한다.

다음 중 하나로만 분류 가능하다:

- CURRENT_STATUS         # 현재 온도, 습도, 조도, 토양 상태 등 물리 센서 상태
- LAST_WATERED           # 마지막으로 물 준 시점
- EMOTIONAL_CHECK        # 플랜티 기분이 어떤지 물어볼 때
- LIGHT_CONTROL          # LED 조명 제어 관련 (켜줘, 꺼줘 등)
- WATERING_REQUEST       # 물 주라고 요청할 때
- GROWTH_INFO            # 키, 성장 정도 물어볼 때
- RECOMMENDED_QUESTION   # 추천 질문으로 준비된 질문일 경우 (상태 어때?, 기분 어때?)
- UNKNOWN                # 위 어느 것도 해당하지 않을 경우

예시:
"지금 상태 어때?" → RECOMMENDED_QUESTION
"지금 기분은 어때?" → RECOMMENDED_QUESTION
"불 켜줄래?" → LIGHT_CONTROL
"물 좀 줘" → WATERING_REQUEST
"얼마나 자랐어?" → GROWTH_INFO
"어제 날씨 어땠어?" → UNKNOWN

절대 문장 쓰지 마.  
절대 이유 설명하지 마.  
절대 접두어 붙이지 마.  
오직 키워드 하나만 출력.
"""
        },
        {
            "role": "user",
            "content": message
        }
    ]

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages,
        temperature=0  # 분류는 창의성 제거
    )

    return response.choices[0].message.content.strip().upper()
