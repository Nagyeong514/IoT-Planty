# ai/planty_voice_agent.py

import os
import pyaudio
import wave
import requests
import tempfile
import time
import struct
import re
from dotenv import load_dotenv
from google.cloud import speech, texttospeech
import pvporcupine

# ✅ 전역 상태 딕셔너리 import
from routes.voicechat_route import voice_shared_state

class PlantyVoiceAgent:
    def __init__(self):
        load_dotenv()

        self.tts_client = texttospeech.TextToSpeechClient()
        self.speech_client = speech.SpeechClient()
        self.porcupine = pvporcupine.create(
            access_key=os.getenv('PICOVOICE_ACCESS_KEY'),
            keyword_paths=["models/planty.ppn"],
            model_path="models/porcupine_params_ko.pv",  # ✅ 한국어 모델 지정
            sensitivities=[0.5]
        )

        self.CHUNK = 512
        self.FORMAT = pyaudio.paInt16
        self.CHANNELS = 1
        self.RATE = 16000

        self.audio = pyaudio.PyAudio()
        self.stream = self.audio.open(
            format=self.FORMAT,
            channels=self.CHANNELS,
            rate=self.RATE,
            input=True,
            frames_per_buffer=self.CHUNK
        )
        self.output_stream = self.audio.open(
            format=self.FORMAT,
            channels=self.CHANNELS,
            rate=self.RATE,
            output=True,
            frames_per_buffer=self.CHUNK
        )

        self.running = True

    def _process_audio_and_transcribe(self):
        voice_shared_state["listening"] = True  # ✅ 듣기 상태 시작

        frames = []
        for _ in range(0, int(self.RATE / self.CHUNK * 4)):
            data = self.stream.read(self.CHUNK, exception_on_overflow=False)
            frames.append(data)

        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmpfile:
            with wave.open(tmpfile.name, "wb") as wf:
                wf.setnchannels(self.CHANNELS)
                wf.setsampwidth(self.audio.get_sample_size(self.FORMAT))
                wf.setframerate(self.RATE)
                wf.writeframes(b"".join(frames))

            with open(tmpfile.name, "rb") as audio_file:
                content = audio_file.read()
            os.unlink(tmpfile.name)

        audio = speech.RecognitionAudio(content=content)
        config = speech.RecognitionConfig(
            encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
            sample_rate_hertz=16000,
            language_code="ko-KR",
            model="latest_long",
            use_enhanced=True
        )

        try:
            response = self.speech_client.recognize(config=config, audio=audio)
            if not response.results:
                return None
            return response.results[0].alternatives[0].transcript
        except Exception as e:
            print(f"[STT 오류] {e}")
            return None
        finally:
            voice_shared_state["listening"] = False  # ✅ 듣기 상태 종료

    def _get_reply_from_backend(self, message):
        try:
            response = requests.post("http://localhost:5000/api/chat", json={"message": message})
            data = response.json()
            return data.get("reply", ""), data.get("face", "happy.png")
        except Exception as e:
            print(f"[GPT 백엔드 오류] {e}")
            return "죄송합니다. 지금은 대화가 어려워요.", "neutral.png"


    def _extract_emotion(self, response):
        match = re.search(r"\[(.*?)\]$", response)
        if match:
            emotion = match.group(1)
            text = response[:match.start()].strip()
        else:
            emotion, text = "neutral", response
        return emotion, text

    def _speak_text(self, text):
        synthesis_input = texttospeech.SynthesisInput(text=text)
        voice = texttospeech.VoiceSelectionParams(
            language_code="ko-KR",
            name="ko-KR-Neural2-A",
            ssml_gender=texttospeech.SsmlVoiceGender.FEMALE
        )
        audio_config = texttospeech.AudioConfig(
            audio_encoding=texttospeech.AudioEncoding.MP3,
            speaking_rate=1.0
        )
        response = self.tts_client.synthesize_speech(
            input=synthesis_input, voice=voice, audio_config=audio_config
        )
        with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as out:
            out.write(response.audio_content)
            tmp_path = out.name
        os.system(f"mpg123 -q {tmp_path}")
        os.unlink(tmp_path)

    def run(self):
        print("[🎙️ 음성 대기 중...] (키워드 감지)")
        while self.running:
            print(".", end="", flush=True)  # ✅ 매 프레임마다 점 찍어보기 (루프 정상 작동 확인용)

            pcm = self.stream.read(self.porcupine.frame_length, exception_on_overflow=False)
            pcm = struct.unpack_from("h" * self.porcupine.frame_length, pcm)
            keyword_index = self.porcupine.process(pcm)
            if keyword_index >= 0:
                print("[📣 키워드 인식됨!] → 음성 입력 시작")
                transcript = self._process_audio_and_transcribe()

                # ✅ STT 결과 업데이트
                voice_shared_state["transcript"] = transcript or ""
                voice_shared_state["reply"] = ""
                voice_shared_state["emotion"] = "neutral"

                if transcript:
                    print(f"[🗣️ 사용자가 말함] {transcript}")
                    reply, face = self._get_reply_from_backend(transcript)
                    print(f"[🤖 GPT 응답] {reply}")
                    print(f"[😊 표정 파일명] {face}")

                    # ✅ 응답 및 표정 상태 반영
                    voice_shared_state["reply"] = reply
                    voice_shared_state["emotion"] = face.replace(".png", "")

                    self._speak_text(reply)
                else:
                    print("[❗ 음성 인식 실패]")

    def stop(self):
        self.running = False
        self.stream.stop_stream()
        self.stream.close()
        self.output_stream.stop_stream()
        self.output_stream.close()
        self.audio.terminate()
        self.porcupine.delete()
