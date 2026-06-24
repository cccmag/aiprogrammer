# GPT-4V 與視覺理解 API 應用

## 前言

GPT-4V（GPT-4 Vision）是 OpenAI 首個支援圖片輸入的多模態模型，能夠根據圖片內容進行問答、分析、推理。本文將介紹如何透過 API 使用 GPT-4V 的視覺理解能力，並展示實際應用場景。

---

## 一、基礎用法

GPT-4V 的 API 接口與文字版 GPT-4 相同，只需要在 `messages` 中加入 `image_url` 類型的內容：

```python
from openai import OpenAI

client = OpenAI(api_key="sk-...")

response = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {
            "role": "user",
            "content": [
                {"type": "text", "text": "請描述這張圖片中的內容"},
                {
                    "type": "image_url",
                    "image_url": {
                        "url": "https://example.com/photo.jpg",
                        "detail": "high"
                    }
                },
            ],
        }
    ],
    max_tokens=500,
)

print(response.choices[0].message.content)
```

## 二、Base64 編碼的圖片

對於本地圖片或需要隱私保護的場景，可以使用 Base64 編碼：

```python
import base64

def encode_image(image_path):
    with open(image_path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")

base64_img = encode_image("screenshot.png")

response = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": "分析這個螢幕截圖中的 UI 元素"
                },
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/png;base64,{base64_img}",
                        "detail": "high"
                    },
                },
            ],
        }
    ],
)
```

## 三、多圖片比較

GPT-4V 可以同時分析多張圖片，適合進行圖片的比較與對比：

```python
messages = [
    {
        "role": "user",
        "content": [
            {"type": "text", "text": "比較這兩張圖片的風格差異"},
            {
                "type": "image_url",
                "image_url": {"url": "https://example.com/design_v1.png"}
            },
            {
                "type": "image_url",
                "image_url": {"url": "https://example.com/design_v2.png"}
            },
        ],
    }
]
```

## 四、視覺理解應用場景

### 4.1 表單與文件解析

```python
def extract_receipt(image_path):
    base64_img = encode_image(image_path)
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": (
                            "請從這張收據中提取以下資訊，用 JSON 格式輸出：\n"
                            "- 商店名稱\n- 日期\n"
                            "- 所有品項及價格\n- 總金額"
                        )
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{base64_img}"
                        }
                    },
                ],
            }
        ],
        response_format={"type": "json_object"},
    )
    return response.choices[0].message.content
```

### 4.2 圖片分類與標註

```python
def classify_product_image(image_path, categories):
    base64_img = encode_image(image_path)
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": (
                            f"將此圖片分類到以下類別之一：{', '.join(categories)}\n"
                            "請只輸出類別名稱。"
                        )
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{base64_img}"
                        }
                    },
                ],
            }
        ],
    )
    return response.choices[0].message.content.strip()
```

## 五、成本考量

GPT-4V 的計價方式取決於 `detail` 參數：

| 參數 | 圖片解析度 | Token 成本 |
|------|-----------|-----------|
| `low` | 512x512 | 85 tokens |
| `high` | 2048x2048 | 170 tokens + 分割成本 |

建議對不需要高精度的場景使用 `detail: "low"` 以降低成本。

---

## 結語

GPT-4V 讓視覺理解變得前所未有的簡單。無需訓練自己的視覺模型，只需呼叫 API 即可獲得強大的圖片分析能力。從文件數位化到自動化測試，GPT-4V 正在成為多模態 AI 應用的事實標準接口。

---

**參考資料**

- OpenAI Vision 指南：https://platform.openai.com/docs/guides/vision
- GPT-4V 系統卡：https://arxiv.org/abs/2303.08774
- 視覺理解 API 應用：https://www.google.com/search?q=GPT-4V+vision+API+applications
- OpenAI 計價頁面：https://openai.com/pricing
