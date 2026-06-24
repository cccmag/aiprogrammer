# 主題程式碼說明

## 程式碼範例結構

本期提供了 GPT-2 文字生成的完整範例，展示如何使用預訓練語言模型進行文字生成任務。

## 檔案列表

- `gpt2_demo.py`：GPT-2 文字生成示範程式

## 依賴套件

```bash
pip install torch transformers
```

## 使用方式

```bash
python3 gpt2_demo.py
```

## 重點函數

### `generate_text(prompt, max_length, temperature)`

- `prompt`：輸入提示文字
- `max_length`：最大生成長度
- `temperature`：生成隨機性（越高越有創造性）

這個函數展示了如何使用 GPT-2 進行文字生成，包括溫度參數對輸出多樣性的影響。

## 練習題

1. 調整 `temperature` 參數，觀察輸出變化
2. 嘗試不同的 `max_length` 值
3. 修改 `top_k` 和 `top_p` 參數，控制生成品質
4. 比較 `gpt2` 與 `gpt2-medium` 的輸出差異

## 參考資源

- https://www.google.com/search?q=GPT-2+text+generation+transformers+Python+example+tutorial
- https://www.google.com/search?q=Hugging+Face+transformers+GPT-2+implementation+code+guide