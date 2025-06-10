# services/save_watering_log.py

from db import get_connection

def save_watering_log(method='manual'):
    conn = get_connection()
    cursor = conn.cursor()
    query = """
        INSERT INTO watering_log (method)
        VALUES (%s)
    """
    cursor.execute(query, (method,))
    conn.commit()
    cursor.close()
    conn.close()
