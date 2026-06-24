# 主題程式碼說明

## 程式碼範例結構

本期提供了 GPT-3 API 使用的完整範例，展示如何利用 Few-shot Learning 能力。

## 檔案列表

- `gpt3_demo.py`：GPT-3 API 使用範例

## 依賴套件

```bash
pip install openai
```

## 使用方式

```bash
python3 gpt3_demo.py
```

## 重點函數

### `call_gpt3(prompt, model="davinci")`

簡化的 GPT-3 API 呼叫包裝。

### `fewshot_translation(example_pairs, input_text)`

展示如何用 Few-shot 進行翻譯。

### `compare_models(prompt)`

比較不同 GPT-3 模型的能力。

## 練習題

1. 申請 OpenAI API key 並測試
2. 設計不同的 Few-shot Prompt 觀察效果
3. 比較不同溫度參數的輸出差異

## 參考資源

- https://www.google.com/search?q=OpenAI+API+GPT-3+Python+tutorial+setup+2020
- https://www.google.com/search?q=few-shot+prompt+design+GPT-3+best+practices+examples