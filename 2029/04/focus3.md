# 語音互動與即時處理（2023-2029）

## 語音模態的獨特性

語音不同於文字與圖像——它是連續的、即時的、富含副語言資訊（語調、情感、節奏）。多模態 Agent 若能理解語音，就能實現更自然的互動。語音互動的最大挑戰在於延遲：人類對話的 acceptable 延遲約 200ms，超過此門檻就會感覺不自然。

## 語音 Agent 架構演進

早期（2023-2024）採用串接式：ASR → LLM → TTS。2025 年後，原生語音模型（如 GPT-4o 語音模式、Gemini Audio）直接處理語音 embedding，延遲大幅降低至 300ms 以內。

```python
import speech_recognition as sr
import pyttsx3
import openai

class VoiceAgent:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.tts = pyttsx3.init()

    def listen_and_respond(self):
        with sr.Microphone() as source:
            audio = self.recognizer.listen(source)
        text = self.recognizer.recognize_whisper(audio)
        response = openai.chat.completions.create(
            model="gpt-4o", messages=[{"role": "user", "content": text}]
        )
        reply = response.choices[0].message.content
        self.tts.say(reply)
        self.tts.runAndWait()
        return reply
```

## 即時處理的關鍵技術

1. **語音活動偵測（VAD）**：判斷人類何時開始／結束說話
2. **串流 ASR**：邊說邊辨識，不必等說完，使用 WebSocket 串流
3. **低延遲 TTS**：2024 年 CosyVoice、XTTS 等模型達到即時合成品質
4. **語音中斷處理**：Agent 說話時人類可打斷，需要即時暫停機制

## 情感感知與語調理解

2025-2026 年，模型開始從語調推斷使用者情緒，使用 SpeechBrain 或自監督模型進行情感辨識：

```python
from speechbrain.inference import EncoderClassifier
classifier = EncoderClassifier.from_hparams(
    source="speechbrain/emotion-recognition-wav2vec2"
)
```

## 多輪語音對話的記憶

語音 Agent 需要處理「上下文延續」問題：使用者可能在一句話中使用「那個」指代之前提到的物件。2026 年後的解決方案是將語音轉錄與多模態記憶整合，讓 Agent 同時記住「說了什麼」與「看到了什麼」，實現真正的多模態對話。

## 參考資源

- https://www.google.com/search?q=real+time+voice+agent+architecture+2024
- https://www.google.com/search?q=GPT-4o+voice+mode+multimodal
- https://www.google.com/search?q=speech+emotion+recognition+agent
