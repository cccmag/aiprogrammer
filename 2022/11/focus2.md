# 基於規則的對話系統

## 設計哲學

基於規則的對話系統遵循符號主義 AI 的核心信念：人類的對話行為可以被歸納為一組有限的規則。系統設計者透過分析對話模式，將常見的對話場景編碼為規則腳本。

## 模式匹配引擎

模式匹配是基於規則系統的核心技術。系統維護一組「模式-回應」對，當使用者輸入匹配某個模式時，系統回傳對應的回應。

```
使用者輸入 → 模式匹配 → 擷取變數 → 填入模板 → 生成回覆
```

ELIZA 使用的模式匹配技術至今仍然優雅：

```
模式: "I am {feeling}"
回應: "How long have you been {feeling}?"
```

## AIML 語言

AIML（人工智慧標記語言）是 Richard Wallace 為 ALICE 機器人設計的 XML 方言。AIML 支援：

- **遞迴匹配**：可以在回覆中嵌入其他模式，形成複雜的對話流程
- **變數替換**：支援 <star/> 語法擷取模式中的變數
- **主題管理**：透過 <that/> 和 <topic/> 標籤管理對話上下文

AIML 範例：

```xml
<category>
    <pattern>I AM *</pattern>
    <template>How long have you been <star/>?</template>
</category>
```

## 優點

- **高度可控**：系統行為完全由設計者決定，不會產生預期外的回覆
- **可解釋性**：每次回應都可以追溯到特定的規則，便於除錯和改進
- **無需訓練資料**：不需要大規模對話語料庫

## 缺點

- **維護成本高**：隨著對話場景增加，規則庫呈指數級增長
- **缺乏泛化能力**：遇到未覆蓋的模式時完全失效
- **對話不自然**：規則的回覆往往顯得生硬和模板化

## 現代應用

雖然純規則系統已經很少用於對話 AI，但規則技術仍然在某些場景中發揮作用：

- **混合系統**：作為深度學習系統的備援和約束機制
- **領域限定場景**：如銀行的簡單查詢、常見問題解答
- **對話流程控制**：管理高層次的對話流程和轉移

## 延伸閱讀

- [AIML 規範](https://www.google.com/search?q=AIML+specification)
- [ALICE 機器人](https://www.google.com/search?q=ALICE+chatbot+AIML)
- [基於規則 vs 機器學習對話](https://www.google.com/search?q=rule+based+vs+machine+learning+chatbot)
