# 本期焦點

## 形式語言與自動機：計算理論的基石

### 引言

形式語言 (Formal Language) 與自動機 (Automata) 理論是計算機科學的基石。從程式語言的編譯器到正則表達式引擎，從自然語言處理到生物資訊學——這些看似不相關的領域，背後都依賴於 1950 年代由 Noam Chomsky、Stephen Kleene、Alan Turing 等先驅建立的理論框架。

Chomsky 在 1956 年提出的語言階層 (Chomsky Hierarchy)，將形式語言分為四大類：正則語言、上下文無關語言、上下文相關語言和遞迴可枚舉語言。每一類語言對應一種自動機模型：有限自動機 (DFA/NFA)、下推自動機 (PDA)、線性有界自動機 (LBA) 和 Turing Machine。

本期雜誌將帶領讀者深入探索這個優雅的理論體系。從最基本的 DFA 開始，逐步建構到通用 Turing Machine，我們不僅討論理論，還提供完整的 Python 實作，讓讀者可以親手驗證這些計算模型的力量。

### 大綱

- [附加：自動機程式實作 — Python 實戰演練](focus_code.md)
  - automata.py：DFA/NFA/Regex/CFG/TM 的完整 Python 實作

1. [形式語言概論：Chomsky 階層](focus1.md)
   - Chomsky 階層與四類語言之定義

2. [正則語言與有限自動機 DFA/NFA](focus2.md)
   - 確定性與非確定性有限自動機

3. [正則表達式與 Kleene 定理](focus3.md)
   - 正則表達式與自動機的等價性

4. [上下文無關語言 CFG](focus4.md)
   - 上下文無關文法與語法樹

5. [下推自動機 PDA](focus5.md)
   - PDA 與上下文無關語言辨識

6. [Turing Machine 與遞迴可枚舉語言](focus6.md)
   - Turing Machine 的定義與計算能力

7. [語言階層與計算能力](focus7.md)
   - 可計算性、可判定性與不可解問題

---

### 濃縮回顧

#### Chomsky 的分類革命

1956 年，語言學家 Noam Chomsky 發表了《Three Models for the Description of Language》，首次提出了形式語言的階層分類。他將語言按照產生規則的複雜度分為四類，每一類都對應一種自動機模型。這個框架不僅影響了語言學，更成為整個計算理論的基礎。

#### 自動機的譜系

從最簡單的 DFA 到最強大的 Turing Machine，自動機的能力逐步增強：
- **DFA/NFA**：有限的記憶，只能識別正則語言
- **PDA**：加上一個堆疊，可以識別上下文無關語言
- **LBA**：線性有界的 Tape，識別上下文相關語言
- **TM**：無限的 Tape，可以識別所有可計算語言

#### Kleene 的連結

Stephen Kleene 在 1956 年證明了正則表達式與有限自動機的等價性，即著名的 Kleene 定理。這個定理說明了描述性語言（正則表達式）與機械性語言（自動機）之間的深層連結。

#### 計算的極限

Turing 在 1936 年提出的停機問題 (Halting Problem) 證明了某些問題是無法用演算法解決的。這個發現不僅是理論上的里程碑，更對實際的程式語言設計、編譯器最佳化、靜態分析等領域產生了深遠影響。

---

### 延伸閱讀

- [形式語言概論](focus1.md)
- [正則語言與有限自動機](focus2.md)
- [正則表達式與 Kleene 定理](focus3.md)
- [上下文無關語言](focus4.md)
- [下推自動機](focus5.md)
- [Turing Machine](focus6.md)
- [語言階層與計算能力](focus7.md)

---

*本期焦點到此結束。下期我們將聚焦機器學習與深度學習的基礎，敬請期待。*
