# 程式碼合成與驗證

## 1. 引言

合成資料不僅包含文字與影像，程式碼也是重要的合成對象。LLM 可以生成大量的程式碼片段作為訓練資料，但程式碼與自然語言最大的不同在於：它必須是可執行的。這使得程式碼合成的驗證成為一個獨特的挑戰。

## 2. 合成程式碼的應用場景

- **程式碼模型訓練**：為 CodeLLaMA、StarCoder 等模型提供訓練資料
- **單元測試生成**：為現有程式碼產生測試案例
- **對抗性測試**：生成邊界案例測試程式碼的穩健性

## 3. 實作：函式合成與測試

```python
import ast
import sys
from openai import OpenAI

client = OpenAI()

def synthesize_function(description: str) -> str:
    """根據描述合成 Python 函式"""
    prompt = f"""請寫一個 Python 函式，功能為：{description}
要求：
1. 包含型別註釋
2. 包含 docstring
3. 處理邊界情況
4. 只回傳程式碼，不要解釋"""
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content

def validate_syntax(code: str) -> bool:
    """驗證程式碼語法正確"""
    try:
        ast.parse(code)
        return True
    except SyntaxError as e:
        print(f"語法錯誤：{e}")
        return False

# 合成一個排序函式
code = synthesize_function("接受整數列表，回傳排序後的列表")
print(code)
print("語法驗證：", "通過" if validate_syntax(code) else "失敗")
```

## 4. 執行驗證

更嚴格的驗證需要實際執行程式碼並測試。可用 `subprocess` 在隔離環境中執行合成程式碼，搭配預先定義的測試案例來驗證正確性。

## 5. 多樣性確保策略

為避免合成資料的單一性，可以在 prompt 中加入風格多樣化指示：

```python
def diverse_synthesis(description: str, style: str) -> str:
    styles = {
        "functional": "使用函數式程式設計風格，避免可變狀態",
        "oop": "使用物件導向風格，封裝在類別中",
        "minimal": "使用最少程式碼，一行內完成"
    }
    prompt = f"""{description}
風格要求：{styles.get(style, styles["functional"])}
回傳純程式碼。"""
    return client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    ).choices[0].message.content
```

## 6. 結語

程式碼合成與驗證是合成資料領域中最「硬」的場景之一。語法驗證、執行測試、多樣性控制三者缺一不可。實務中建議建立自動化 CI 管道，對每一次合成結果進行編譯與測試。

## 延伸閱讀

- [OpenAI Codex](https://www.google.com/search?q=OpenAI+Codex+code+generation)
- [Program Synthesis Overview](https://www.google.com/search?q=program+synthesis+techniques+machine+learning)
