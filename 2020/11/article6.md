# AlphaFold2：蛋白質折疊預測的重大突破

## 前言

2020 年 11 月，DeepMind 的 AlphaFold2 在 CASP14（蛋白質結構預測關鍵評估）競賽中取得了革命性的突破，解決了困擾生物學家 50 年的蛋白質折疊問題。

## CASP14 競賽結果

```
CASP14 結果（2020 年 11 月）：
────────────────────────────────

AlphaFold2 GDT 分數：92.4/100
- 達到實驗室精度水準
- 顯著領先其他團隊
- 其他方法 GDT 分數普遍低於 60

評估標準：
- GDT（Global Distance Test）：衡量預測結構與實際結構的相似度
- 90+ 分數 = 實驗品質
```

## 技術突破

### AlphaFold2 架構

```python
"""
AlphaFold2 核心創新：

1. Evoformer 區塊
   - 多序列對齊（MSA）注意力
   - 配對表示學習
   
2. 結構模組
   - 直接預測 3D 座標
   - 不動點迭代

3. 端到端訓練
   - 從序列到結構
   - 損失函數直接基於結構
"""
```

### 注意力機制的應用

```
AlphaFold2 中的創新：
────────────────────────────────

1. MSA 注意力
   - 學習胺基酸之間的進化關係
   - 捕捉長程交互

2. 幾何學習
   - 直接操作 3D 座標
   - 遵守物理約束

3.置信度預測
   - pLDDT：每殘基置信度
   - PAE：成對置信度
```

## 對科學的影響

### 藥物開發加速

```
傳統藥物開發：
研究新藥 → 10-15 年

AlphaFold2 之後：
- 快速預測蛋白質結構
- 大幅減少實驗時間
- 加速藥物靶點發現
```

### 開源影響

```
DeepMind 的開放：
────────────────────────────────

2021 年：
- AlphaFold DB 開放（人類蛋白質組）
- 數百萬結構公開存取
- 極大推動生命科學研究
```

## 延伸閱讀

- [AlphaFold2 論文](https://www.google.com/search?q=AlphaFold2+Nature+2021+paper)
- [DeepMind AlphaFold 頁面](https://www.google.com/search?q=DeepMind+AlphaFold+protein+folding)
- [CASP14 結果](https://www.google.com/search?q=CASP14+protein+structure+prediction+results)

---

*本篇文章為「AI 程式人雜誌 2020 年 11 月號」文章集錦之一。*

（編者註：這是 2020 年 11 月的重大 AI 事件，請特別關注。）