# 語音與音訊 AI 技術（2016-2026）

## 從序列到序列到統一模型

語音 AI 的發展經歷了從傳統訊號處理到深度學習，再到統一多模態模型的演進。與視覺和語言不同，語音處理有其獨特的挑戰：**時間序列的連續性**、**說話者變異**、**背景噪音**。

## 三大核心任務

### 1. 自動語音辨識（ASR）

2022 年 Whisper 是轉折點——在大規模弱監督資料（68 萬小時多語言）上訓練，支援辨識、翻譯、語言偵測等多任務：

```python
def whisper_input(audio_path):
    """音訊 → Log-Mel Spectrogram（80 維梅爾頻譜）"""
    audio = librosa.load(audio_path, sr=16000)[0]
    return np.log(librosa.feature.melspectrogram(y=audio, n_mels=80) + 1e-10).T
```

### 2. 語音合成（TTS）

從文字生成語音。WaveNet（2016）開啟深度學習 TTS 時代，現代模型（VITS、XTTS）採用編碼器-聲學模型-聲碼器三階段：

```python
def tts_generate(text):
    tokens = tokenize(text)
    mel = acoustic_model(tokens)
    return vocoder(mel)  # 波形輸出
```

### 3. 語音事件偵測（SED）

辨識環境音、情緒、說話者：

辨識說話者、情緒、背景音、音樂等非語音事件。

## 語音+視覺+文字：多模態語音

語音 AI 的最新趨勢是與其他模態結合：

```
傳統 ASR：音訊 → 文字

多模態語音：
  音訊 ─┐
         ├→ 統一模型 → 文字 + 情緒 + 說話者 + 環境
  視覺 ─┘  (看著說話者的嘴形)
  
  AV-HuBERT：音訊 + 視覺唇形 → 更好的語音理解
```

```python
def av_transcribe(audio, video):
    """音訊 + 視覺（唇形）→ 更準確的語音辨識"""
    a_feat = audio_encoder(audio)
    v_feat = video_encoder(video)  # 唇形特徵
    return decoder(cross_attention(a_feat, v_feat))
```

## 語音 AI 里程碑

| 年份 | 模型 | 領域 | 創新 |
|------|------|------|------|
| 2016 | WaveNet | TTS | 深度學習語音生成 |
| 2018 | Tacotron 2 | TTS | 端到端語音合成 |
| 2019 | Wav2Vec 2.0 | ASR | 自監督語音表示 |
| 2021 | HuBERT | ASR | 隱藏單元 BERT |
| 2022 | Whisper | ASR | 多語言大規模 ASR |
| 2023 | AudioLDM | 生成 | 文字生成音訊 |
| 2024 | Voicebox | TTS | 語音修復與編輯 |
| 2025 | 多模態語音 | 融合 | 音+視+文的統一模型 |
| 2026 | 即時口譯系統 | 翻譯 | 端到端語音翻譯 |

## 小結

語音 AI 從傳統訊號處理走向深度學習，再由單一模態走向多模態融合。Whisper 證明了「規模化弱監督」在語音中的威力，而多模態語音則展示了視覺資訊在噪音環境下的關鍵幫助。語音是最自然的互動介面，也將是多模態 AI 的重要入口。

---

**下一步**：[多模態 RAG](focus5.md)

## 延伸閱讀

- [Whisper 論文](https://www.google.com/search?q=Whisper+Robust+Speech+Recognition+via+Large+Scale+Weak+Supervision)
- [Wav2Vec 2.0 論文](https://www.google.com/search?q=Wav2Vec+2.0+Self+Supervised+Learning+of+Speech+Representations)
- [AudioLDM 論文](https://www.google.com/search?q=AudioLDM+Text+to+Audio+Generation)
