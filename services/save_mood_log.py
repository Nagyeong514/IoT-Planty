# services/save_mood_log.py

from db import get_connection

def save_mood_log(mood_type, face_expression, reason):
    conn = get_connection()
    cursor = conn.cursor()
    query = """
        INSERT INTO mood_log (mood_type, face_expression, reason)
        VALUES (%s, %s, %s)
    """
    cursor.execute(query, (mood_type, face_expression, reason))
    conn.commit()
    cursor.close()
    conn.close()
