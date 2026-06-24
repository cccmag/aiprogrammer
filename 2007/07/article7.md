# 語音辨識進展：sphinx-4 語音識別系統

## 概述

2007 年，CMU Sphinx 專案發布了 Sphinx-4，這是一個完全由 Java 編寫的語音識別系統。Sphinx-4 的出現，為研究者和開發者提供了一個靈活、強大且可擴展的語音識別研究平台。

## 語音識別基礎

### 語音識別流程

典型語音識別系統的處理流程：

```
聲音訊號 → 前處理 → 特徵提取 → 解碼 → 文字輸出
              ↓
         分框、加窗、FFT
              ↓
         MFCC/PLP 特徵
              ↓
         聲學模型 + 語言模型
```

### 關鍵技術

1. **特徵提取** -- MFCC（梅爾倒譜系數）
2. **聲學模型** -- GMM-HMM 或 DNN-HMM
3. **語言模型** -- N-gram 模型
4. **解碼器** -- Viterbi 演算法或束搜索

## Sphinx-4 架構

### 核心元件

```java
// Sphinx-4 語音識別配置
Configuration configuration = new Configuration();

// 設定模型路徑
configuration.setAcousticModelPath("resource:/edu/cmu/sphinx/models/en-us/en-us");
configuration.setDictionaryPath("resource:/edu/cmu/sphinx/models/en-us/cmudict-en-us.dict");
configuration.setLanguageModelPath("resource:/edu/cmu/sphinx/models/en-us/en-us.lm.bin");

// 建立識別器
StreamSpeechRecognizer recognizer = new StreamSpeechRecognizer(configuration);
recognizer.startRecognition(System.in);

// 進行識別
SpeechResult result = recognizer.getResult();
System.out.println("辨識結果: " + result.getHypothesis().getBestPronunciationResult());
```

### 設定麥克風輸入

```java
// 即時語音識別
public class LiveSpeechRecognizer {
    private StreamSpeechRecognizer recognizer;
    private boolean stopped = false;

    public void startRecognition() {
        Configuration config = new Configuration();
        // ... 設定配置

        recognizer = new StreamSpeechRecognizer(config);
        recognizer.startRecognition(System.in);

        // 取得麥克風音訊輸入
        AudioSystem audioSystem = AudioSystem.getInstance();
        Microphone mic = audioSystem.getMicrophone();
        mic.startRecording();

        // 持續識別直到收到停止命令
        while (!stopped) {
            SpeechResult result = recognizer.getResult();
            if (result != null) {
                String text = result.getHypothesis().getBestFinalResult();
                System.out.println("聽到: " + text);
            }
        }

        mic.stopRecording();
        recognizer.stopRecognition();
    }
}
```

### 自訂語言模型

```java
// 建立自訂語言模型
LanguageModelGenerator generator = new LanguageModelGenerator();
BinaryLMFSReader writer = new BinaryLMFSReader();

try {
    // 從文字檔案生成語言模型
    Model textModel = generator.generateText(LANGUAGE_MODEL_INPUT, LANGUAGE_MODEL_TYPE);
    BinaryLMFSWriter.saveBinary(textModel, OUTPUT_PATH);
} catch (IOException e) {
    // 處理錯誤
}
```

## Sphinx-4 的特性

### 1. 完全 Java 實現

Sphinx-4 完全使用 Java 編寫，具有以下優勢：
- 跨平台相容性
- 易於與 Java 應用整合
- 良好的物件導向設計

### 2. 模組化架構

```java
// 可以替換不同的元件
FrontEnd frontEnd = new FrontEnd() {
    // 自訂前處理
};

Recognizer recognizer = new Recognizer(frontEnd, acousticModel, languageModel);
```

### 3. 支援多種解碼模式

```java
// 詳細模式 - 傳回多個候選
Lattice lattice = decoder.decode();
List<WordResult> nbest = lattice.getNbest(10);

// 即時模式
StreamDataSource dataSource = new StreamDataSource();
FrontEnd frontEnd = new FrontEnd(dataSource);
```

## 應用場景

### 1. 語音命令控制

```java
// 語音命令識別
String[] commands = { "開始", "停止", "暫停", "繼續", "結束" };

SpeechResult result = recognizer.getResult();
String recognized = result.getHypothesis().getBestPronunciationResult();

for (String command : commands) {
    if (recognized.contains(command)) {
        executeCommand(command);
        break;
    }
}
```

### 2. 語音輸入

```java
// 將語音轉換為文字
public String convertSpeechToText(AudioInputStream audio) {
    StreamSpeechRecognizer recognizer = setupRecognizer();
    recognizer.startRecognition(audio);

    StringBuilder text = new StringBuilder();
    SpeechResult result;

    while ((result = recognizer.getResult()) != null) {
        text.append(result.getHypothesis().getBestPronunciationResult());
        text.append(" ");
    }

    recognizer.stopRecognition();
    return text.toString();
}
```

### 3. 語音日記

```java
// 持續錄音和識別
public class VoiceDiary {
    public void startRecording() {
        Microphone mic = AudioSystem.getInstance().getMicrophone();
        StreamSpeechRecognizer recognizer = createRecognizer();

        mic.startRecording();
        recognizer.startRecognition(mic.getStream());

        while (isRecording) {
            SpeechResult result = recognizer.getResult();
            if (result != null) {
                String text = result.getHypothesis().getBestFinalResult();
                saveToDiary(text);
            }
        }

        mic.stopRecording();
    }
}
```

## 效能與限制

### 效能優化

```java
// 使用更大詞典的語言模型
configuration.setLanguageModelPath("models/en-us-wide.lm");

// 使用特定領域的模型
configuration.setDictionaryPath("models/medical.dict");
configuration.setLanguageModelPath("models/medical.lm");
```

### 限制

1. **準確率** -- 依賴於訓練資料和收音品質
2. **計算需求** -- 即時識別需要足夠的處理能力
3. **領域限制** -- 通用模型在特定領域表現較差

## 結語

Sphinx-4 為語音識別研究和應用開發提供了一個開放且強大的平台。雖然現代的深度學習方法（如 RNN-T、Transformer）已經大幅提升了語音識別的準確率，但 Sphinx-4 的模組化設計和開源精神，對後續語音識別技術的發展產生了深遠影響。

---

*延伸閱讀：*
- [CMU Sphinx 官方網站](https://developers.google.com/search/?q=cmusphinx+official)
- [Sphinx-4 文件](https://developers.google.com/search/?q=sphinx4+documentation)