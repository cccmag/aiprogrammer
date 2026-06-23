# Whisper 語音辨識實戰

## 前言

OpenAI Whisper 是一個開源的自動語音辨識（ASR）模型，支援 99 種語言的轉錄與翻譯。Whisper 採用 Encoder-Decoder 架構，在大量的弱監督資料上訓練，展現出驚人的泛化能力。本文將示範如何使用 Whisper 進行語音辨識、翻譯與自訂微調。

---

## 一、安裝與基礎使用

```bash
pip install openai-whisper
```

最簡單的用法只需兩行程式碼：

```python
import whisper

model = whisper.load_model("base")
result = model.transcribe("meeting_recording.mp3")
print(result["text"])
```

## 二、模型大小選擇

Whisper 提供五種模型尺寸，在速度與準確度之間取捨：

```python
models = {
    "tiny":   {"params": "39M",  "speed": "最快",  "accuracy": "低"},
    "base":   {"params": "74M",  "speed": "快",    "accuracy": "中"},
    "small":  {"params": "244M", "speed": "中",    "accuracy": "良"},
    "medium": {"params": "769M", "speed": "慢",    "accuracy": "優"},
    "large":  {"params": "1550M","speed": "最慢",  "accuracy": "最佳"},
}

def transcribe_with_timing(audio_path, model_name="base"):
    import time
    model = whisper.load_model(model_name)
    start = time.time()
    result = model.transcribe(audio_path)
    elapsed = time.time() - start
    print(f"模型: {model_name}, 耗時: {elapsed:.2f}s")
    return result["text"]
```

## 三、進階參數

Whisper 提供多種參數來自訂轉錄行為：

```python
result = model.transcribe(
    "chinese_speech.mp3",
    language="zh",           # 指定語言
    task="transcribe",       # 或 "translate"（翻譯成英文）
    temperature=0.0,         # 貪婪解碼（穩定但可能不夠多樣）
    compression_ratio_threshold=2.4,
    logprob_threshold=-1.0,
    no_speech_threshold=0.6,
    verbose=True,            # 顯示逐段時間戳
)
```

### 3.1 分段輸出與時間戳

```python
for segment in result["segments"]:
    start = segment["start"]
    end = segment["end"]
    text = segment["text"]
    print(f"[{start:6.2f}s -> {end:6.2f}s] {text}")
```

### 3.2 語言偵測

Whisper 可以自動偵測音訊語言：

```python
audio = whisper.load_audio("mixed_lang.mp3")
audio = whisper.pad_or_trim(audio)
mel = whisper.log_mel_spectrogram(audio).to(model.device)

_, probs = model.detect_language(mel)
print(f"偵測語言: {max(probs, key=probs.get)}")
```

## 四、語音翻譯（Speech-to-Text Translation）

Whisper 可以直接將非英文語音翻譯成英文：

```python
# 中文語音直接轉英文文字
result = model.transcribe("chinese_lecture.mp3", task="translate")
print(result["text"])  # 輸出為英文
```

## 五、Whisper 的程式化呼叫

```python
from whisper import load_model, load_audio, pad_or_trim, log_mel_spectrogram, decode
from whisper.decoding import DecodingOptions, DecodingResult

model = load_model("small")

audio = load_audio("interview.wav")
audio = pad_or_trim(audio)
mel = log_mel_spectrogram(audio).to(model.device)

options = DecodingOptions(
    language="zh",
    task="transcribe",
    without_timestamps=True,
)
result: DecodingResult = model.decode(mel, options)
print(result.text)
```

## 六、微調 Whisper

對於特定領域（如醫學、法律），微調可以顯著提升準確率：

```python
from datasets import load_dataset
from transformers import (
    WhisperProcessor, WhisperForConditionalGeneration,
    Seq2SeqTrainingArguments, Seq2SeqTrainer
)

processor = WhisperProcessor.from_pretrained("openai/whisper-small")
model = WhisperForConditionalGeneration.from_pretrained("openai/whisper-small")

# 準備資料集
dataset = load_dataset("your_custom_asr_dataset")
def prepare_dataset(batch):
    audio = batch["audio"]
    inputs = processor(
        audio["array"], sampling_rate=audio["sampling_rate"],
        text=batch["transcription"], return_tensors="pt"
    )
    return inputs

# 訓練
training_args = Seq2SeqTrainingArguments(
    output_dir="./whisper-finetuned",
    per_device_train_batch_size=8,
    learning_rate=1e-5,
    num_train_epochs=3,
)

trainer = Seq2SeqTrainer(
    model=model,
    args=training_args,
    train_dataset=dataset.map(prepare_dataset),
)
trainer.train()
```

---

## 結語

Whisper 的開源本質和強大效能使其成為語音辨識領域的首選方案。無論是即時轉錄、會議記錄還是跨語言翻譯，Whisper 都能勝任。結合 Hugging Face 的生態系統，微調自訂領域模型也變得相當容易。

---

**參考資料**

- Whisper 論文：https://arxiv.org/abs/2212.04356
- OpenAI Whisper GitHub：https://github.com/openai/whisper
- Whisper 模型比較：https://www.google.com/search?q=whisper+model+sizes+comparison
- Hugging Face Whisper 文檔：https://huggingface.co/docs/transformers/model_doc/whisper
