# services/save_sensor_data.py

from db import get_connection

def save_sensor_data(temperature, humidity, soil_dry, light):
    conn = get_connection()
    cursor = conn.cursor()
    query = """
        INSERT INTO sensor_log (temperature, humidity, soil_dry, light)
        VALUES (%s, %s, %s, %s)
    """
    cursor.execute(query, (temperature, humidity, soil_dry, light))
    conn.commit()
    cursor.close()
    conn.close()
