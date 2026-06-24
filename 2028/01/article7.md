# 提示詞工程 for Code

## 1. 引言

提示詞工程（Prompt Engineering）在程式碼生成場景中有其獨特的挑戰與技巧。與自然語言提示不同，程式碼提示需要更高的精確度——一個字元偏差就可能導致語法錯誤或邏輯錯誤。本文將深入探討針對程式碼生成的提示詞設計策略。

## 2. 結構化提示

程式碼生成的最佳提示結構：

```
角色定義: 你是 Python 專家。
任務描述: 實作一個 LRU Cache。
輸入輸出格式: function lru_cache(capacity: int) -> class
限制條件: 時間複雜度 O(1)，執行緒安全。
範例: cache = lru_cache(2); cache.put(1,1); cache.get(1) -> 1
```

這種結構化提示的關鍵要素：

1. **角色設定**：明確的專家角色有助於模型選擇正確的技術棧
2. **任務邊界**：什麼該做、什麼不該做
3. **格式規範**：輸入輸出型別、函式簽名
4. **範例驅動**：few-shot 範例比描述更有效

## 3. 鏈式思考（Chain-of-Thought）for Code

程式碼生成的 CoT 與自然語言不同，更接近「逐步規劃實作」：

```python
# 不好的提示：直接要求實作
"實作一個快速排序"

# 好的提示：引導逐步思考
"請逐步思考快速排序的實作：
1. 選擇 pivot 的策略（第一個元素、隨機、三數取中）
2. 分割邏輯（Lomuto 或 Hoare）
3. 遞迴終止條件
4. 就地排序或回傳新陣列
然後實作程式碼"
```

## 4. 約束編碼技巧

### 4.1 型別約束

在提示中包含型別註釋可以顯著提升生成品質：

```python
from typing import List, Optional

def binary_search(arr: List[int], target: int) -> Optional[int]:
    """實現二分搜尋，回傳目標索引或 None"""
```

### 4.2 測試先行（Test-First Prompting）

在提示中先寫測試，讓模型實作符合測試的程式碼：

```python
# 請實作一個函式滿足以下測試：
assert calculate("1+2") == 3
assert calculate("2*3+4") == 10
assert calculate("(1+2)*3") == 9
```

## 5. 常用提示模板

| 場景 | 模板 |
|------|------|
| 新增函式 | `實作函式 {signature}，功能為 {description}` |
| 重構 | `重構 {code}，保持相同功能但提升 {readability/performance}` |
| 轉譯 | `將 {code} 從 {lang_a} 轉換為 {lang_b}` |
| 解釋 | `解釋 {code} 的每一行在做什麼` |
| 除錯 | `這段程式碼有 bug：{code}。錯誤訊息：{error}` |

## 6. 常見陷阱

1. **過度指定**：強迫模型使用特定的演算法，可能忽略了更適合的方案
2. **不明確的邊界**：沒有指定輸出的格式，導致模型回傳難以解析的結果
3. **忽略上下文**：沒有提供相關的專案結構或工具鏈
4. **遺忘錯誤處理**：沒有要求模型考慮邊界情況

## 7. 結語

程式碼提示詞工程是一門不斷演進的學問。核心原則是：**明確勝於模糊、結構勝於自由、範例勝於描述**。2026 年的最佳實踐強調「雙向校準」——開發者需要學會如何寫提示，AI 也需要學會如何提問來澄清需求。未來，提示詞將從「指令」進化為「對話」，AI 不再被動執行，而是主動確認。

---

## 延伸閱讀

- [Prompt Engineering Guide](https://www.google.com/search?q=prompt+engineering+guide+code+generation)
- [ChatGPT Prompt Engineering for Developers](https://www.google.com/search?q=ChatGPT+prompt+engineering+for+developers)
- [Chain-of-Thought Prompting 論文](https://www.google.com/search?q=chain+of+thought+prompting+paper)
- [程式碼提示詞最佳實踐](https://www.google.com/search?q=code+prompt+engineering+best+practices+LLM)
