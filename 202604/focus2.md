# 高階編譯器的誕生：FORTRAN 與第一個編譯器（1950s-1960s）

## FORTRAN 的革命

1957 年，IBM 發布了 FORTRAN（Formula Translation）編譯器——這是世界上第一個真正實用的高階語言編譯器。它的誕生標誌著程式設計從機器導向轉向人類導向的歷史性轉折。

### 時代背景

1950 年代中期，電腦仍然非常昂貴且難以程式設計。IBM 704 是當時最先進的科學計算電腦，但程式設計師需要用組合語言或機器碼來為它寫程式。IBM 的客戶（主要是科學家和工程師）抱怨程式設計太慢、太容易出錯。

John Backus 當時是 IBM 的年輕程式設計師，他帶領一個團隊開始了一個大膽的專案——創造一個「自動程式設計系統」。

### 懷疑與反對

在 FORTRAN 專案啟動之初，許多人對編譯器持懷疑態度：

> 「電腦不可能自動生成高效的機器碼。人類程式設計師的智慧是無可取代的。」—— 1950 年代的主流觀點

當時的普遍質疑包括：

1. **效能問題**：編譯器生成的程式碼不可能比手工優化的組合語言快
2. **記憶體問題**：編譯器本身就會消耗大量記憶體
3. **可靠性問題**：自動生成的程式碼難以除錯

Backus 團隊用了三年時間證明這些質疑是錯的。

## John Backus 與 BNF

### John Backus 的貢獻

John Backus（1924-2007）是美國計算機科學家，FORTRAN 的發明者。他在計算機科學史上留下了兩大革命性貢獻：

1. **FORTRAN**（1957）：第一個高階程式語言的編譯器
2. **BNF 表示法**（1959）：一種描述程式語言語法的形式化方法

有趣的是，Backus 最初在密西根大學學的是化學，後來轉學到哥倫比亞大學學數學。他對程式設計的興趣始於 IBM 的技術工作。

### BNF 表示法

1959 年，在 ALGOL 58 的設計會議上，Backus 提出了一種用數學方式描述語法的方法——後來由 Peter Naur 完善，稱為 BNF（Backus-Naur Form）。

```
// BNF 語法規則範例

<expression> ::= <term> | <expression> "+" <term>
<term>       ::= <factor> | <term> "*" <factor>
<factor>     ::= <number> | "(" <expression> ")"
<number>     ::= <digit> | <digit> <number>
<digit>      ::= "0" | "1" | "2" | "3" | "4" | "5" | "6" | "7" | "8" | "9"

// 這意味著：
// expression 可以是 term 或 expression + term
// term 可以是 factor 或 term * factor
// factor 可以是 number 或 ( expression )
```

BNF 的革命性在於：

1. **精確性**：消除了語法描述中的模糊性
2. **形式化**：為編譯器設計提供了數學基礎
3. **遞迴**：用遞迴規則描述無限集的語法

BNF 直接啟發了後來的 Lex 和 Yacc——詞法分析器和語法分析器的自動生成工具。

## FORTRAN 編譯器的設計與實現

### 團隊陣容

Backus 的團隊由 13 人組成，其中包括：

- **John Backus**：專案領導者
- **Irving Ziller**：程式設計師
- **Robert Nelson**：程式設計師
- **Roy Nutt**：IBM 704 專家

這個團隊在當時被稱為「The FORTRAN Project」，他們的工作從 1954 年持續到 1957 年。

### 編譯器架構

FORTRAN 編譯器採用多遍掃描（Multi-pass）架構：

```
原始碼 (FORTRAN)
      │
      ▼
┌─────────────┐
│  第 1 遍     │  詞法分析、語法分析
│  (Lexical)  │
└──────┬──────┘
       ▼
┌─────────────┐
│  第 2 遍     │  語義分析、符號表建立
│  (Semantic) │
└──────┬──────┘
       ▼
┌─────────────┐
│  第 3 遍     │  中間程式碼生成
│  (IR Gen)   │
└──────┬──────┘
       ▼
┌─────────────┐
│  第 4 遍     │  最佳化（常量摺疊等）
│  (Optimize) │
└──────┬──────┘
       ▼
┌─────────────┐
│  第 5 遍     │  目標程式碼生成
│  (Code Gen) │
└──────┬──────┘
       ▼
     機器碼
```

### 創新的最佳化技術

FORTRAN 編譯器引入了多項至今仍在使用的編譯最佳化技術：

**1. 常量摺疊（Constant Folding）：**

```fortran
C 原始碼
      X = 3.14159 * 2.0

C 編譯器直接計算為
      X = 6.28318
```

**2. 通用子表達式消除（Common Subexpression Elimination）：**

```fortran
C 原始碼
      A = B * C + D
      E = B * C + F

C 編譯器優化為
      T = B * C
      A = T + D
      E = T + F
```

**3. 暫存器分配（Register Allocation）：**

FORTRAN 編譯器會自動將常用變數分配給 IBM 704 的硬體暫存器，避免頻繁的記憶體存取。

### 對效能的極致追求

Backus 團隊非常重視編譯器生成程式碼的品質。他們設定的目標是：

> 「編譯器生成的程式碼至少能達到手寫組合語言的 80% 效能。」

最終，FORTRAN 編譯器生成的程式碼達到了約 90% 的效能，有些情況下甚至超過了手工程式碼。這徹底打消了人們對編譯器的疑慮。

## FORTRAN 的影響

### 對程式設計的影響

FORTRAN 的成功帶來了巨大的連鎖效應：

1. **生產力革命**：程式設計效率提升了數倍到數十倍
2. **可移植性**：同一個 FORTRAN 程式可以在不同型號的電腦上執行
3. **程式碼理解**：高階語言比組合語言更容易理解和維護
4. **科學計算普及**：科學家和工程師可以親自寫程式，不需要依賴專業程式設計師

### 一個經典的 FORTRAN 程式

```fortran
C 計算費波那契數列
      PROGRAM FIBONACCI
      INTEGER N, I, F1, F2, F3
      PRINT *, '請輸入項數:'
      READ *, N
      F1 = 0
      F2 = 1
      DO 10 I = 1, N
         F3 = F1 + F2
         PRINT *, I, F3
         F1 = F2
         F2 = F3
10    CONTINUE
      STOP
      END
```

### FORTRAN 的版本演進

| 版本 | 年份 | 特點 |
|------|------|------|
| FORTRAN I | 1957 | 第一個版本 |
| FORTRAN II | 1958 | 加入副程式、函式 |
| FORTRAN IV | 1962 | 標準化版本 |
| FORTRAN 66 | 1966 | ANSI 標準 |
| FORTRAN 77 | 1978 | 結構化程式設計 |
| Fortran 90 | 1991 | 陣列運算、模組 |
| Fortran 95 | 1995 | 現代化 |
| Fortran 2003 | 2004 | 物件導向 |
| Fortran 2018 | 2018 | 並行運算增強 |

## 其他早期編譯器

### ALGOL 編譯器

ALGOL（Algorithmic Language）是 1958 年由歐洲和美國的計算機科學家共同設計的語言。雖然 ALGOL 本身在商業上並不成功，但它對編譯器理論的貢獻是巨大的：

1. **BNF 語法描述**：首次用形式化方法定義語言
2. **區塊結構**：引入了變數的作用域概念
3. **遞迴**：首次支援遞迴呼叫
4. **傳名呼叫（Call by Name）**：Jensen 裝置

### COBOL 編譯器

COBOL（Common Business-Oriented Language）於 1959 年設計，專注於商業資料處理：

```cobol
       IDENTIFICATION DIVISION.
       PROGRAM-ID. HELLO.
       ENVIRONMENT DIVISION.
       DATA DIVISION.
       WORKING-STORAGE SECTION.
       01 NAME    PIC A(20).
       01 OUTPUT  PIC Z(10).
       PROCEDURE DIVISION.
           DISPLAY "YOUR NAME: ".
           ACCEPT NAME.
           DISPLAY "HELLO, " NAME.
           STOP RUN.
```

COBOL 編譯器的特點：
- 語法接近英語，對商業使用者友善
- 強大的檔案處理能力
- 至今仍有大量遺留系統運行 COBOL

### Lisp 編譯器

Lisp 的編譯器有其獨特性——由於 Lisp 的同像性（Homoiconicity），編譯器本身就可以用 Lisp 來寫：

```lisp
;; Lisp 編譯器的核心 eval 函式
(defun eval (exp env)
  (cond
    ((numberp exp) exp)
    ((symbolp exp) (lookup exp env))
    ((eq (car exp) 'quote) (cadr exp))
    ((eq (car exp) 'lambda) (list 'closure (cadr exp) (caddr exp) env))
    ((eq (car exp) 'if) (if (eval (cadr exp) env)
                            (eval (caddr exp) env)
                            (eval (cadddr exp) env)))
    (t (apply (eval (car exp) env)
              (mapcar (lambda (arg) (eval arg env)) (cdr exp))))))
```

## 結語

FORTRAN 的成功證明了編譯器不僅可行，而且高效。它開啟了程式語言和編譯器設計的黃金時代。在接下來的二十年裡，編譯器理論迅速成熟，從一門藝術轉變為一門科學。

下一篇文章將介紹 1960-70 年代編譯器理論的黃金時代——詞法分析、語法分析與語義分析的理論基礎。

---

## 延伸閱讀

- [Backus 1957: The FORTRAN Automatic Coding System](https://www.google.com/search?q=Backus+FORTRAN+automatic+coding+system+1957)
- [BNF 表示法](https://www.google.com/search?q=Backus+Naur+form+BNF)
- [FORTRAN 發展史](https://www.google.com/search?q=history+of+FORTRAN)

---

*本篇文章為「AI 程式人雜誌 2026 年 4 月號」歷史回顧系列之二。*
