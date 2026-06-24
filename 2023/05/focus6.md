# Turing Machine 與遞迴可枚舉語言

## 計算的終極模型

在 Chomsky 階層的頂端是 Type-0 語言——遞迴可枚舉語言 (Recursively Enumerable Language)，對應的計算模型是 Turing Machine (TM)。Alan Turing 在 1936 年的開創性論文《On Computable Numbers, with an Application to the Entscheidungsproblem》中提出了這個模型，從根本上定義了「可計算性」的邊界。

Turing Machine 的結構非常簡單，但其計算能力是所有已知計算模型中最強的。Church-Turing 論題指出：任何直觀上可計算的函數都可以被某個 Turing Machine 計算。

## Turing Machine 的定義

一個 Turing Machine 由七元組 (Q, Σ, Γ, δ, q0, B, F) 定義：

- Q：狀態的有窮集合
- Σ：輸入字母表（不包含空白符號 B）
- Γ：磁帶字母表（Σ ∪ {B} ⊆ Γ）
- δ：轉移函數，δ: Q × Γ → Q × Γ × {L, R}
- q0：起始狀態
- B：空白符號 (Blank)
- F：接受狀態集合

TM 有一個無限長的磁帶 (Tape) 和一個讀寫頭 (Head)。每一步操作中，TM 根據當前狀態和讀寫頭指向的符號，決定下一個狀態、寫入的符號、以及讀寫頭的移動方向（左或右）。

## Turing Machine 的能力

儘管結構簡單，Turing Machine 可以模擬任何計算：

1. **算術運算**：加法、減法、乘法、除法
2. **邏輯判斷**：比較、分支
3. **資料操作**：複製、搜尋、排序
4. **模擬其他 TM**：通用 Turing Machine (UTM)

一個關鍵概念是：TM 的「程式」就是其轉移函數 δ。不同的 δ 定義不同的 TM，就像不同的程式碼定義不同的功能。

## 範例：辨識 {a^n b^n c^n}

語言 L = {a^n b^n c^n | n ≥ 0} 是上下文相關語言（Type-1），需要 TM 來辨識：

1. 掃描磁帶，找到第一個 a，將其標記為已處理
2. 移動到第一個 b，標記為已處理
3. 移動到第一個 c，標記為已處理
4. 重複以上過程，直到所有符號都被處理
5. 如果處理過程中任何一步找不到對應的符號，則拒絕

這個範例展示了 TM 如何利用磁帶的讀寫能力來追蹤複雜的計數關係。

## 遞迴可枚舉語言

語言 L 是遞迴可枚舉的 (Recursively Enumerable)，若存在一個 TM 可以在有限時間內接受 L 中的所有字串（但對不屬於 L 的字串可能永不終止）。

語言 L 是遞迴的 (Recursive)，若存在一個 TM 可以在有限時間內判定任何字串是否屬於 L（總會終止並給出正確答案）。

所有的遞迴語言都是遞迴可枚舉的，但反之不真。存在一些語言是遞迴可枚舉的但不是遞迴的——這正是停機問題的根源。

## Church-Turing 論題

Church-Turing 論題指出：Turing Machine 能夠計算的函數集合，恰好與我們直觀上認為「可計算」的函數集合一致。這個論題不是定理（無法被證明），但被計算機科學界廣泛接受。

這個論題的一個重要推論是：如果一個問題不能被 Turing Machine 解決，那麼沒有任何計算機——包括未來的量子電腦——能夠解決它。

## 參考資料

- [https://www.google.com/search?q=Turing+machine+definition+computation](https://www.google.com/search?q=Turing+machine+definition+computation)
- [https://www.google.com/search?q=Church+Turing+thesis+computability+theory](https://www.google.com/search?q=Church+Turing+thesis+computability+theory)
- [https://www.google.com/search?q=Turing+Machine+模擬+程式](https://www.google.com/search?q=Turing+Machine+模擬+程式)
