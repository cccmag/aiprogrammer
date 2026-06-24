# Google 翻譯 API：機器翻譯的開放時代

## 概述

2007 年，Google 推出了翻譯 API（Google Translate API），為開發者提供了便利的機器翻譯服務。這項服務的開放，標誌著機器翻譯技術從學術研究走向大眾應用的重要一步，也為日後更多基於翻譯的應用程式奠定了基礎。

## 機器翻譯的發展背景

### 早期方法

機器翻譯經歷了多個發展階段：

1. **規則式翻譯 (RBMT)** -- 使用語言學規則和字典
2. **範例式翻譯 (EBMT)** -- 從範例庫中匹配相似句子
3. **統計式翻譯 (SMT)** -- 從大量雙語語料庫中學習翻譯機率

### Google 翻譯的技術

Google 翻譯在 2007 年採用了統計式機器翻譯（SMT）技術：

```python
"""
統計式機器翻譯概念展示
實際的翻譯系統要複雜得多
"""

def demo():
    print("=" * 50)
    print("機器翻譯系統概念展示")
    print("=" * 50)

    # 翻譯模型概念
    print("\n--- 統計式機器翻譯 ---")
    print("""
統計式機器翻譯的核心思想：
- 訓練階段：從大量雙語語料庫學習
- 翻譯階段：使用學習到的機率進行翻譯

P(英文 | 中文) = P(中文 | 英文) * P(英文) / P(中文)

翻譯模型：P(f|e) - 英文句子 e 翻譯成中文句子 f 的機率
語言模型：P(e) - 英文句子 e 出現的機率
""")

    # 翻譯範例
    print("\n--- 翻譯範例 ---")
    translations = [
        ("Hello", "你好", 0.95),
        ("Good morning", "早上好", 0.92),
        ("How are you?", "你好嗎？", 0.88),
        ("Thank you", "謝謝", 0.97),
    ]

    for original, translated, prob in translations:
        print(f"{original} → {translated} (機率: {prob:.2%})")

    # API 呼叫概念
    print("\n--- API 呼叫概念 ---")
    api_example = """
# 典型的翻譯 API 呼叫
response = translate_api.translate(
    text="Hello world",
    source="en",
    target="zh-TW"
)
# 回傳: {"translatedText": "你好世界"}

# 批次翻譯
response = translate_api.translate_batch([
    {"text": "Hello", "source": "en", "target": "zh-TW"},
    {"text": "Goodbye", "source": "en", "target": "zh-TW"}
])
"""
    print(api_example)

    print("\n" + "=" * 50)

if __name__ == "__main__":
    demo()