# services/save_mood_log.py

from db import get_connection

def save_mood_log(mood_type, face_expression, reason, temperature, humidity, soil_dry, light):
    conn = get_connection()
    cursor = conn.cursor()
    query = """
        INSERT INTO mood_log (
            mood_type,
            face_expression,
            reason,
            temperature,
            humidity,
            soil_dry,
            light
        ) VALUES (%s, %s, %s, %s, %s, %s, %s)
    """
    cursor.execute(query, (
        mood_type,
        face_expression,
        reason,
        temperature,
        humidity,
        soil_dry,
        light
    ))
    conn.commit()
    cursor.close()
    conn.close()
