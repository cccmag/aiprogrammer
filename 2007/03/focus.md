# 本期焦點

## 程式語言多樣化的興起

### 引言

2007 年是程式語言發展史上特別有趣的一年。經過多年的沉寂，程式語言領域正在經歷一場文藝復興。動態語言的興起、函數式編程的回歸、以及傳統語言的創新，共同塑造了一個多元化的時代。

本期內容將帶您回顧這段激動人心的時光，探索從 Python 到 Ruby，從 JavaScript 到 Haskell，各種語言如何改變了我們的計算世界。

---

## 大綱

* [程式：動態語言程式設計實作](focus_code.md)
   - Python vs Ruby 語法對比
   - 動態類型與鸭子型別

1. [動態語言的復興：Python、Ruby 的崛起](focus1.md)
   - Python 的哲學
   - Ruby 的優雅

2. [PHP 的繁榮：Web 開發的主流選擇](focus2.md)
   - PHP 的生態系
   - WordPress 現象

3. [JavaScript 的重生：AJAX 時代的主角](focus3.md)
   - 從客戶端腳本到全端語言

4. [Java 與 JVM 平台的演進](focus4.md)
   - Java SE 6 的改進
   - JVM 語言的繁榮

5. [.NET 與 C# 的發展](focus5.md)
   - C# 3.0 的創新

6. [函數式語言的興起](focus6.md)
   - Haskell 與 Scala

7. [未來展望：程式語言的下一個十年](focus7.md)
   - 語言發展趨勢

---

## 濃縮回顧

### 程式語言的分類

```
┌────────────────────────────────────────────────────────┐
│              程式語言分類圖                             │
├────────────────────────────────────────────────────────┤
│                                                        │
│  編譯型 vs 解釋型：                                    │
│  - C/C++ → 編譯後執行                                 │
│  - Python/Ruby → 直譯執行                             │
│                                                        │
│  靜態型別 vs 動態型別：                                │
│  - Java/C# → 編譯時檢查型別                           │
│  - Python/Ruby → 執行時檢查型別                       │
│                                                        │
│  命令式 vs 函數式：                                    │
│  - C/Java → 命令式                                   │
│  - Haskell/Scala → 函數式                             │
│                                                        │
│  物件導向 vs 原型繼承：                                │
│  - Java/C++ → 類別系統                               │
│  - JavaScript → 原型鏈                                │
│                                                        │
└────────────────────────────────────────────────────────┘
```

### 2007 年語言趨勢

```
動態語言的崛起信號：
┌────────────────────────────────────────────────────────┐
│                                                        │
│  - Ruby on Rails 展示了 Ruby 的潛力                   │
│  - Google 使用 Python 於內部                         │
│  - PHP 繼續統治 Web 開發                              │
│  - JavaScript 成為全端語言                            │
│  - PHP → Python 的遷移                               │
│                                                        │
└────────────────────────────────────────────────────────┘
```

---

## 語法對比

### Python vs Ruby

```python
# Python
def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)

# Ruby
def fibonacci(n)
    return n if n <= 1
    fibonacci(n-1) + fibonacci(n-2)
end
```

### JavaScript 範例

```javascript
// 現代 JavaScript
const fibonacci = (n) => {
    if (n <= 1) return n;
    return fibonacci(n-1) + fibonacci(n-2);
};
```

---

## 結論

2007 年是程式語言多樣化的轉捩點。動態語言的興起、函數式編程的回歸、以及傳統語言的創新，共同開創了一個多元化的時代。

---

## 延伸閱讀

- [Python 官方網站](focus1.md)
- [Ruby 官方網站](focus2.md)
- [JavaScript 歷史](focus3.md)

---

*本期焦點到此結束。*