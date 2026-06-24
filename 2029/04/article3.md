# 語音互動 Agent

## 1. 語音管線

語音 Agent 需要 ASR（語音辨識）、NLU（語義理解）、TTS（語音合成）三階段。2025 年後端到端模型簡化了流程。

## 2. ASR 與語音轉文字

```python
import whisper

class SpeechAgent:
    def __init__(self):
        self.asr = whisper.load_model("base")
        self.llm = __import__("openai").OpenAI()

    def listen_and_respond(self, audio_path):
        text = self.asr.transcribe(audio_path)["text"]
        resp = self.llm.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": f"使用者說：{text}\n請回覆"}]
        )
        return resp.choices[0].message.content
```

## 3. 文字轉語音

現代 TTS 支援情緒控制，讓回覆更人性化：

```python
from openai import OpenAI

def speak(text, voice="alloy", emotion="neutral"):
    prefix = {"happy": "用開心的語氣說："}.get(emotion, "")
    client = OpenAI()
    resp = client.audio.speech.create(model="tts-1", voice=voice, input=prefix + text)
    resp.stream_to_file("response.mp3")
```

## 4. 即時雙向對話

完整語音 Agent 需處理打斷與輪換：

```python
class RealtimeVoiceAgent:
    def conversation_loop(self):
        while True:
            if self.detect_speech():
                audio = self.record_until_silence()
                text = self.asr.transcribe(audio)["text"]
                if "結束" in text:
                    break
                reply = self.llm.chat(...)
                self.speak(reply)
```

## 5. 結語

瓶頸不再是模型能力，而是即時管線延遲。端到端語音模型將是 2027 年的突破方向。

- https://www.google.com/search?q=whisper+ASR+real+time+agent
- https://www.google.com/search?q=OpenAI+TTS+API+agent+integration
