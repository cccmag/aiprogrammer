# 形式語言概論：Chomsky 階層

## 什麼是形式語言？

形式語言 (Formal Language) 是一個由有限字母表 (Alphabet) 上的字串所組成的集合。與自然語言（如中文、英文）不同，形式語言的精確定義來自於嚴格的數學規則——文法 (Grammar)。

一個形式文法 G 由四個部分組成：G = (V, T, P, S)，其中 V 是非終止符號集合、T 是終止符號集合、P 是產生規則集合、S 是起始符號。

## Chomsky 階層

1956 年，Noam Chomsky 根據產生規則的形式，將文法分為四種類型：

### Type-3：正則文法 (Regular Grammar)

產生規則的形式為 A → aB 或 A → a（右線性），或 A → Ba 或 A → a（左線性）。正則文法對應的是最簡單的語言類別——正則語言。這種語言可以用有限自動機 (DFA/NFA) 來辨識，也可以在 O(n) 時間內完成匹配。

**範例**：二進位偶數的語言 L = { w ∈ {0,1}* | w 以 0 結尾 }

```
S → 0S | 1S | 0
```

### Type-2：上下文無關文法 (Context-Free Grammar)

產生規則的形式為 A → γ，其中 γ 是任意符號序列。上下文無關文法對應上下文無關語言，可以用下推自動機 (PDA) 辨識。這是描述程式語言語法的主要工具。

**範例**：匹配括號的語言 L = { a^n b^n | n ≥ 0 }

```
S → aSb | ε
```

### Type-1：上下文相關文法 (Context-Sensitive Grammar)

產生規則的形式為 αAβ → αγβ，其中 γ ≠ ε。這意味著產生式的應用依賴於上下文。上下文相關語言可以用線性有界自動機 (LBA) 辨識。

**範例**：L = { a^n b^n c^n | n ≥ 0 }

```
S → aSBC | aBC
CB → BC
aB → ab
bB → bb
bC → bc
cC → cc
```

### Type-0：無限制文法 (Unrestricted Grammar)

產生規則無任何限制，形式為 α → β，其中 α ≠ ε。無限制文法對應遞迴可枚舉語言，可以用 Turing Machine 辨識。這是計算能力最強的語言類別，但同時也意味著某些問題是不可判定的。

## Chomsky 階層的包含關係

這四類語言的關係是嚴格的包含關係：

**Type-3 ⊂ Type-2 ⊂ Type-1 ⊂ Type-0**

也就是說，一切正則語言都是上下文無關語言，反之不真；一切上下文無關語言都是上下文相關語言，反之不真；以此類推。

這個包含關係告訴我們：語言的表達能力是有層次的。越外層的語言越強大，但同時其辨識演算法也越複雜，甚至在某些情況下不可判定。

## 為什麼學習 Chomsky 階層？

理解 Chomsky 階層對於程式設計師有幾個重要的實際意義：

1. **正則表達式 vs 解析器**：知道何時該用正則表達式（Type-3）、何時該用完整的解析器（Type-2）
2. **編譯器設計**：編譯器的詞法分析器（Type-3）和語法分析器（Type-2）分別對應不同的語言類別
3. **問題難度評估**：了解一個問題屬於哪一類語言，可以幫助判斷解決方案的可行性和效率

## 參考資料

- [https://www.google.com/search?q=Chomsky+hierarchy+formal+languages](https://www.google.com/search?q=Chomsky+hierarchy+formal+languages)
- [https://www.google.com/search?q=Noam+Chomsky+1956+three+models](https://www.google.com/search?q=Noam+Chomsky+1956+three+models)
- [https://www.google.com/search?q=Chomsky+階層+形式語言](https://www.google.com/search?q=Chomsky+階層+形式語言)
