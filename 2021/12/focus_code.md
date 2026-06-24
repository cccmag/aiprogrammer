# 程式碼說明 — focus_code.md

## 概述

本期範例程式碼位於 `_code/ai_review.py`，展示 2021 年 AI 發展的核心概念和模擬實現。涵蓋語言模型、對比學習、強化學習基礎等概念的教學實現。程式碼使用純 Python，幫助讀者建立 AI 技術的直覺。

## 元件說明

### `SimpleLanguageModel`

實現簡化的語言模型概念，基於 GPT 系列的下一代預測思想。雖然規模和真實模型相差甚遠，但展示了語言模型的核心原理。

### `ContrastiveLearning`

實現對比學習的簡化版本。通過讓相似樣本接近、不相似樣本遠離來學習表示，這是自監督學習的重要方法。

### `RewardModel`

模擬強化學習中的獎勵模型，用於 RLHF（人類回饋強化學習）。簡化了從人類偏好中學習獎勵信號的過程。

### `AttentionMechanism`

實現簡化的 Transformer 注意力機制。展示如何通過加權求和整合不同位置的資訊，這是現代 AI 架構的核心。

### `NeuralNetwork`

提供一個通用的神經網路框架，支援前饋傳播和反向傳播，用於演示各類 AI 模型的基礎構建塊。

## 執行程式

```bash
cd _code
bash test.sh
```

`test.sh` 使用 `set -x` 顯示執行過程並呼叫 `python3 ai_review.py`。`demo()` 函式展示完整流程：語言模型預測、對比學習表示、注意力機制運作，驗證 2021 年 AI 核心概念的正確運作。

## 參考資源

- OpenAI 官方：https://www.google.com/search?q=OpenAI+research+2021
- DeepMind 官方：https://www.google.com/search?q=DeepMind+publications+2021
- Hugging Face：https://www.google.com/search?q=Hugging+Face+Transformers+2021