# Python 在科學計算的崛起

## 從 Fortran 到 Python

科學計算的世界曾經是 Fortran、C 和 MATLAB 的天下。1990 年代，研究人員習慣於撰寫 Fortran 程式進行數值模擬，或使用 MATLAB 進行快速原型開發。然而沒有一位科學家能夠預見，一種以簡潔語法著稱的通用程式語言，會在二十年後徹底改變科學計算的面貌。

Python 在科學計算的旅程始於 1995 年，當時 Jim Hugunin 發布了 **Numeric** 套件——這是 Python 的第一個多維陣列實現。Hugunin 原本在 MIT 攻讀博士，他創建 Numeric 的目的是將 Python 的易用性與 Fortran 的效能結合。

```
1995 ── Numeric (Jim Hugunin)
2005 ── NumPy (Travis Oliphant) 合併 Numeric + Numarray
2008 ── Pandas (Wes McKinney)
2011 ── scikit-learn (INRIA 團隊)
2014 ── Jupyter Notebook
2017 ── PyTorch 發布
2022 ── 資料科學生態全面成熟
```

## Python 為何勝出？

### 語言設計優勢

Python 的設計哲學——簡潔、可讀、明確——恰好符合科學家對程式碼的需求。不同於 C++ 的複雜記憶體管理或 MATLAB 的封閉生態，Python 讓研究人員可以專注於問題本身而非程式語言的細節。

### 膠水語言的威力

現代科學計算需要結合多種語言。Python 作為膠水語言，可以輕鬆地呼叫 C、C++、Fortran、CUDA 等底層實作，同時保持上層 API 的一致性。NumPy 的底層是 C 和 Fortran（LAPACK/BLAS），Pandas 的核心演算法用 Cython 和 C 編寫，scikit-learn 大量使用 Cython。

### 開源社群的推動

不同於 MATLAB 的商業封閉模式，Python 科學計算完全由開源社群推動。這意味著：
- **零成本**：任何人都可以免費使用
- **透明度**：所有演算法原始碼都可檢視
- **可重現性**：研究結果可以完全重現
- **協作**：全球頂尖研究者共同貢獻

## 生態系統的形成

Python 資料科學的成功不僅僅是因為單一函式庫，而是因為整個生態系統的協同效應。核心貢獻者 Travis Oliphant、Wes McKinney、Fernando Pérez 等人各自創建了互補的工具。

```
NumPy  ──→ 提供陣列基礎
  │
  ├──→ SciPy    ──→ 科學計算函數
  ├──→ Pandas   ──→ 資料處理
  ├──→ Matplotlib ──→ 視覺化
  └──→ scikit-learn ──→ 機器學習
```

這種分層設計的優點在於每個函式庫可以專注於自己的領域，同時透過 NumPy 陣列進行無縫資料交換。

## 今日的地位

2022 年的今天，Python 已經成為資料科學的事實標準：

- **學術界**：大部分科學論文使用 Python 進行資料分析
- **業界**：從 Google 到小型新創，Python 是資料基礎設施的核心
- **教育**：大學課程紛紛將 Python 列為第一程式語言

根據 IEEE Spectrum 和 TIOBE 等指數，Python 在 2021-2022 年穩居最受歡迎程式語言首位，其中資料科學應用的成長是主要推動力。

## 延伸閱讀

- [NumPy 官方歷史](https://www.google.com/search?q=NumPy+history+Python)
- [Travis Oliphant 的 NumPy 故事](https://www.google.com/search?q=Travis+Oliphant+NumPy+story)
- [Python 在科學計算的演進](https://www.google.com/search?q=Python+in+scientific+computing+history)

---

*本篇文章為「AI 程式人雜誌 2022 年 3 月號」歷史回顧系列之一。*
