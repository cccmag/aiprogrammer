# ELIZA：第一個聊天機器人

## 1966 年的革命

在幾乎沒有人聽說過「聊天機器人」這個概念的時代，MIT 教授 Joseph Weizenbaum 開發了一個名為 ELIZA 的程式，從此人機互動的歷史被改寫。

## 設計理念

ELIZA 的名字源自 Bernard Shaw 的戲劇《Pygmalion》中的角色 Eliza Doolittle，暗示這個程式像一個正在學習語言的人。ELIZA 模擬的是 Rogerian 心理治療師——這種治療風格的特色是透過反問來引導病人自己發現問題。

Weizenbaum 選擇這個場景的原因非常務實：心理治療的對話主題相對有限（家庭、感情、工作），且治療師的角色主要是反映和提問，這使得模式匹配技術剛好適用。

## 技術核心

ELIZA 的核心是一個稱為 DOCTOR 的腳本，包含約 200 條模式匹配規則。每個規則包含一個模式（pattern）和一個回應模板（template）：

```
PATTERN: "I am {feeling}"
RESPONSE: "How long have you been {feeling}?"

PATTERN: "My {family_member} is {trait}"
RESPONSE: "Tell me more about your {family_member}"
```

### 關鍵技術

ELIZA 不僅做簡單的模式匹配，它還實作了幾個先進的概念：

1. **關鍵詞優先**：當多個模式同時匹配時，優先選擇包含關鍵詞的模式
2. **變數保存**：記錄使用者曾提到的重要資訊，在後續的對話中可再次使用
3. **轉移規則**：當對話陷入死胡同時，自動轉移到預先設計的子對話

## ELIZA 效應

ELIZA 效應是指人們傾向於將人類特質賦予計算機系統的現象。Weizenbaum 發現，即使他的秘書完全了解 ELIZA 的運作原理，她仍然在與 ELIZA 對話時表現出情感投入。

這個現象對後來的 AI 設計產生了深遠影響：系統的可信度和使用者的投入程度不僅取決於技術能力，還取決於互動的設計方式。

## 歷史影響

ELIZA 雖然技術簡單，但它證明了即使是最基本的模式匹配也能創造出令人信服的對話體驗。它奠定了整個對話系統領域的基礎，其影響延續至今：

- 確立了模式匹配作為對話系統的基本技術
- 展示了對話互動的心理學維度
- 引發了關於 AI 倫理和人類-機器關係的討論

## 延伸閱讀

- [ELIZA 原始論文](https://www.google.com/search?q=ELIZA+Weizenbaum+1966)
- [ELIZA 效應](https://www.google.com/search?q=ELIZA+effect+psychology)
- [Joseph Weizenbaum 生平](https://www.google.com/search?q=Joseph+Weizenbaum+MIT+ELIZA)
