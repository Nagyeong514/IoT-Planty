# services/save_led_log.py

from db import get_connection

def save_led_log(mode, state):
    conn = get_connection()
    cursor = conn.cursor()
    query = """
        INSERT INTO led_log (mode, state)
        VALUES (%s, %s)
    """
    cursor.execute(query, (mode, state))
    conn.commit()
    cursor.close()
    conn.close()
