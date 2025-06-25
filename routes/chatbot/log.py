# routes/chatbot/log.py

from services.save_mood_log import save_mood_log

def maybe_save_mood_log(log_data):
    if log_data is None:
        return
    save_mood_log(
        mood_type=log_data["mood_type"],
        face_expression=log_data["face"],
        reason=log_data["text"],
        temperature=log_data["temperature"],
        humidity=log_data["humidity"],
        soil_dry=log_data["soil_dry"],
        light=log_data.get("light")  # optional
    )
