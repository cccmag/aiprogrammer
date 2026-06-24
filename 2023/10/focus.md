# 本期焦點

## 機器學習理論基礎

### 引言

機器學習的驚人成功往往讓人們忽略了一個根本問題：**它為什麼有效？** 為什麼在訓練資料上學到的模型能對未見過的資料做出準確預測？這種泛化能力從何而來？

機器學習理論（Statistical Learning Theory）正是回答這些問題的學科。它不僅提供了理解學習演算法的數學框架，更為設計更好的演算法提供了指導原則。

本期將從七個核心主題深入機器學習理論的基礎：

- **學習問題的形式化**：什麼是「學習」的數學定義？
- **PAC 學習理論**：Probably Approximately Correct 框架
- **VC 維度**：衡量假說空間複雜度的關鍵工具
- **偏差-變異權衡**：模型複雜度的核心矛盾
- **正則化理論**：如何控制模型複雜度
- **核方法**：從線性到非線性的優雅跳躍
- **貝氏學習**：不確定性的量化與更新

### 學習理論的歷史脈絡

學習理論可以追溯到 1960 年代：

| 時間 | 貢獻 | 人物 |
|------|------|------|
| 1960s | 感知機收斂定理 | Rosenblatt |
| 1971 | VC 維度 | Vapnik, Chervonenkis |
| 1984 | PAC 學習框架 | Valiant |
| 1992 | 核技巧 | Boser, Guyon, Vapnik |
| 1990s | 結構風險最小化 | Vapnik |
| 2000s | Rademacher 複雜度 | Bartlett, Mendelson |
| 2010s | 深度學習理論 | 多位研究者 |

### 為什麼學習理論重要

在深度學習主導的時代，學習理論的重要性不減反增：

1. **解釋泛化**：為什麼過參數化模型不 overfitting？這正是現代學習理論的核心問題
2. **指導設計**：正則化、核函數、架構選擇——理論提供了設計原則
3. **理解極限**：哪些問題是「不可學習的」？這告訴我們不該浪費時間
4. **量化不確定性**：貝氏方法和 PAC-Bayes 提供了信心區間

### 核心不等式

學習理論的核心是一類泛化不等式（Generalization Bounds）：

```
R(h) ≤ R̂(h) + Complexity(H) / √n
```

其中 R(h) 是真實風險，R̂(h) 是經驗風險，Complexity(H) 是假說空間的複雜度量，n 是樣本數。

本期將逐步推導這些不等式，並解釋每項的含義。

### 從理論到實踐

```
理論概念 → 統計量 → 演算法原則 → 實際演算法
  |           |          |            |
VC維度       ERM        SRM        SVM
偏差-變異    Rademacher  正則化      Ridge/Lasso
核再生空間   特徵映射    核技巧      Kernel SVM
貝氏定理     後驗分布    MAP        高斯過程
```

**下一步**：[程式實作](focus_code.md) → [學習問題的形式化](focus1.md)

## 延伸閱讀

- [Statistical Learning Theory (Vapnik)](https://www.google.com/search?q=Statistical+Learning+Theory+Vapnik)
- [Foundations of Machine Learning (Mohri)](https://www.google.com/search?q=Foundations+of+Machine+Learning+Mohri)
- [Understanding Machine Learning (Shalev-Shwartz)](https://www.google.com/search?q=Understanding+Machine+Learning+Shalev+Shwartz)
- [An Introduction to Statistical Learning](https://www.google.com/search?q=An+Introduction+to+Statistical+Learning)
