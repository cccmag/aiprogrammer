# 強型別 vs 弱型別

## 型別安全的光譜

### 定義

**強型別（Strong Typing）** 和 **弱型別（Weak Typing）** 描述語言對型別間操作的限制程度。與靜態/動態不同（焦點在檢查時機），強/弱關注的是**型別安全**的嚴格程度。

**強型別**：語言嚴格限制不同型別之間的操作，禁止或要求明確轉換。

**弱型別**：語言允許不同型別之間的隱式轉換，可能在無預警的情況下改變值的型別。

### 經典例子

```python
# Python（強型別）
"hello" + 42  # TypeError: 不允許字串和整數相加
"hello" + str(42)  # "hello42"（需明確轉換）
```

```javascript
// JavaScript（弱型別）
"hello" + 42  // "hello42"（整數被隱式轉為字串）
"5" - 3       // 2（字串被隱式轉為整數）
[] + []       // ""（空陣列變成空字串）
```

### 型別安全的光譜

| 語言 | 強度 | 特色 |
|------|------|------|
| Haskell | 極強 | 無隱式轉換，Maybe 處理空值 |
| Rust | 極強 | 所有權系統防止記憶體錯誤 |
| Python | 強 | 少數隱式轉換（int→float） |
| Java | 強 | 基礎型別間有隱式拓寬 |
| C# | 強 | 可設定 checked/unchecked 上下文 |
| C | 中弱 | void* 繞過型別系統 |
| JavaScript | 弱 | == 運算子有複雜的隱式轉換規則 |
| PHP | 弱 | 字串和數字在比較時自動轉換 |

### 隱式轉換的危險

弱型別語言中常見的陷阱：

```javascript
// JavaScript
0 == false    // true（驚人！）
0 == ""       // true
"" == false   // true
null == undefined // true

// 使用 === 避免隱式轉換
0 === false   // false
```

### 強型別的優勢

1. **更少的執行時期錯誤**：型別不匹配在開發時就被發現
2. **更可預測的行為**：沒有隱式轉換帶來的驚喜
3. **更好的重構支援**：編譯器可以檢查型別變更的影響

### 弱型別的論點

1. **程式碼更簡潔**：不需要明確轉換型別
2. **靈活性更高**：可以混合不同型別的值
3. **快速原型**：不需要關心型別的細節

### 型別強度的趨勢

現代語言普遍傾向於更強的型別安全：

- **TypeScript** 在 JavaScript 之上增加了靜態型別檢查
- **Python** 的型別提示允許在檢查工具層面加強型別
- **Kotlin** 解決了 Java 的 null 安全問題
- **Swift** 從 Objective-C 的動態型別轉向強型別

### 延伸閱讀

- [強型別 vs 弱型別](https://www.google.com/search?q=strong+typing+vs+weak+typing)
- [JavaScript 型別轉換](https://www.google.com/search?q=JavaScript+type+coercion+rules)
