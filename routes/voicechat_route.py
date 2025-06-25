# routes/voicechat_route.py

from flask import Blueprint, Response, stream_with_context
import time
import json

voice_bp = Blueprint('voice', __name__)

# 전역 상태 (다른 파일에서 갱신됨)
voice_shared_state = {
    "listening": False,
    "transcript": "",
    "reply": "",
    "emotion": "neutral"
}

def sse_format(data):
    return f"data: {json.dumps(data)}\n\n"

@voice_bp.route('/api/voice/state')
def stream_voice_state():
    def event_stream():
        while True:
            data = dict(voice_shared_state)            
            data["face"] = f"{data['emotion']}.png" 
                
            yield sse_format(data)                      
            time.sleep(1)

    return Response(stream_with_context(event_stream()), mimetype='text/event-stream')
