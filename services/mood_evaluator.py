# services/mood_evaluator.py


from db import get_connection

def evaluate_mood(temperature, humidity, soil_dry, light, led_state):
    """
    센서값을 기반으로 식물의 현재 기분(mood)을 평가합니다.
    가능한 상태: lovely, hot, cold, angry, confused, cry, happy
    """

    # 1. lovely: 완벽한 생장 환경
    if (
        temperature is not None and 20 <= temperature <= 28 and
        humidity is not None and 60 <= humidity <= 70 and
        soil_dry is False and
        light == 'bright'
    ):
        return {
            "mood_type": "lovely",
            "face": "lovely.png",
            "text": "완벽한 환경이에요, 너무 행복해요! 🌸",
            "reason": "적정 온도·습도에 토양도 촉촉하고 밝아요!"
        }

    # 2. hot
    if temperature is not None and temperature >= 30:
        return {
            "mood_type": "hot",
            "face": "hot.png",
            "text": "햇빛이 너무 뜨거워서 덥네요 ☀️",
            "reason": "온도가 30도 이상이에요"
        }

    # 3. cold
    if temperature is not None and temperature <= 15:
        return {
            "mood_type": "cold",
            "face": "cold.png",
            "text": "오늘은 너무 추워요... 🥶",
            "reason": "온도가 15도 이하예요"
        }

    # 4. angry: 물 부족 (건조 + 습도 낮음)
    if soil_dry == 1 and humidity is not None and humidity <= 30:
        return {
            "mood_type": "angry",
            "face": "angry.png",
            "text": "물이 부족해서 힘들어요... 🥺",
            "reason": "토양이 건조하고 습도도 낮아요"
        }

    # example (추가 방어코드)
    if light not in ['bright', 'dark']:
        light = 'unknown'
        
    # 5. confused: 어두운데 불도 꺼짐
    if light == 'dark' and led_state == 'off':
        return {
            "mood_type": "confused",
            "face": "confused.png",
            "text": "너무 어두워서 혼란스러워요 🌑",
            "reason": "주변이 어두운데 LED도 꺼져있어요"
        }

    # 6. cry: 자주 건조했던 상태
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT soil_dry FROM sensor_log
        ORDER BY timestamp DESC
        LIMIT 3
    """)
    recent = cursor.fetchall()
    cursor.close()
    conn.close()

    dry_count = sum(1 for r in recent if r["soil_dry"] == 1)
    if dry_count >= 2:
        return {
            "mood_type": "cry",
            "face": "cry.png",
            "text": "요즘 계속 건조해서 속상해요... 😢",
            "reason": "최근 3회 중 2번 이상 건조했어요"
        }

    # 7. 기본 상태: happy
    return {
        "mood_type": "happy",
        "face": "happy.png",
        "text": "식무리가 아주 건강해요 😊",
        "reason": "전체적으로 상태가 양호해요"
    }
