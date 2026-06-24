# 程式語意學

## 操作的意義是什麼？

### 什麼是程式語意學？

程式語意學（Program Semantics）研究程式碼的意義——如何精確描述一個程式的行為。語意學為程式語言提供嚴格的數學基礎，是編譯器最佳化、程式驗證和語言設計的理論基石。

### 三種語意學派別

**1. 操作語意（Operational Semantics）**

透過抽象的狀態機描述程式的執行過程。最常見的形式是**結構化操作語意**（Structural Operational Semantics, SOS），也稱為**小步語意**（Small-step Semantics）：

```
⟨E1 + E2, σ⟩ → ⟨E1' + E2, σ'⟩  如果 ⟨E1, σ⟩ → ⟨E1', σ'⟩
⟨n1 + n2, σ⟩ → ⟨n3, σ⟩         如果 n3 = n1 + n2
```

**大步語意（Big-step Semantics）** 直接描述從表達式到最終結果的求值：

```
⟨n, σ⟩ ⇓ n
⟨E1, σ⟩ ⇓ n1, ⟨E2, σ⟩ ⇓ n2
──────────────────────────
⟨E1 + E2, σ⟩ ⇓ n3          (n3 = n1 + n2)
```

**2. 指稱語意（Denotational Semantics）**

將每個程式結構映射到某個數學物件（指稱）。程式 P 的指稱 ⟦P⟧ 是它對應的數學函數：

```
⟦n⟧ = n
⟦E1 + E2⟧ = ⟦E1⟧ + ⟦E2⟧
⟦λx. E⟧ = λx. ⟦E⟧
```

指稱語意的關鍵是**組合性（compositionality）**——整個程式的意義由其子部分的意義組合而成。

**3. 公理語意（Axiomatic Semantics）**

用邏輯公式描述程式的行為規範——前置條件（pre-condition）和後置條件（post-condition）。最著名的是 **Hoare 邏輯**：

```
{P} S {Q}
```

這表示：如果前置條件 P 在執行 S 之前成立，則 S 執行後 Q 成立。

### Hoare 邏輯的規則

```
{P} skip {P}                    (skip 規則)
{P[x:=E]} x := E {P}            (賦值規則)
{P} S1 {Q}, {Q} S2 {R}         (順序組合)
────────────────────
{P} S1; S2 {R}

{B ∧ P} S {Q}, {¬B ∧ P} T {Q}  (條件規則)
────────────────────────────
{P} if B then S else T {Q}

{I ∧ B} S {I}                   (迴圈規則不變式)
────────────────────────
{I} while B do S {I ∧ ¬B}
```

### 程式驗證的實務應用

- **Rust 的所有權系統**：基於線性型別（affine types）的形式化驗證
- **Ada/SPARK**：基於 Hoare 邏輯的合約式程式設計
- **Frama-C**：C 程式的靜態分析工具，使用 ACSL（ANSI/ISO C Specification Language）
- **TLA+**：分散式系統的形式規格語言

### 延伸閱讀

- [操作語意](https://www.google.com/search?q=operational+semantics+programming)
- [指稱語意](https://www.google.com/search?q=denotational+semantics)
- [Hoare 邏輯](https://www.google.com/search?q=Hoare+logic+axiomatic+semantics)

---

*本期焦點到此結束。下一期的主題敬請期待。*
