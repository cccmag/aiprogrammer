# AlphaFold2：蛋白質折疊預測的突破

## 前言

2020 年 11 月，DeepMind 的 AlphaFold2 在 CASP14（蛋白質結構預測關鍵評估）競賽中取得了革命性的突破，解決了困擾生物學家 50 年的蛋白質折疊問題。

## 蛋白質折疊問題

### 什麼是蛋白質折疊？

```
蛋白質折疊：
────────────────────────────────

胺基酸序列 → 折疊 → 3D 結構 → 功能

密碼：AUG CGU UUC GAC...
          ↓（翻譯）
蛋白質：Met-Arg-Phe-Asp...
          ↓（折疊）
3D結構：   ___/|___   ← 複雜的 3D 形狀
          /     \
         |       |
          \_____/

問題：如何從序列預測 3D 結構？
```

### 為什麼這麼重要？

蛋白質的 3D 結構決定了其功能：

```
結構 → 功能：
────────────────────────────────

胰島素受體    → 調節血糖
抗體         → 辨識病原體
酶           → 加速化學反應
離子通道     → 傳遞訊號

結構錯誤 → 功能失常 → 疾病
```

## AlphaFold2 的突破

### CASP14 競賽

CASP（Critical Assessment of protein Structure Prediction）是蛋白質結構預測領域最重要的競賽，每兩年舉辦一次：

```
CASP14 結果（2020 年）：
────────────────────────────────

AlphaFold2：
  - GDT 分数：92.4/100（專業實驗團隊平均 ~90）
  - 中位數準確率：實驗等級 ◄───── 突破性進展
  - 對某些蛋白質：幾乎完美預測

其他團隊：
  - 其他方法的 GDT 分數：~40-60
  - 距離實驗精度有明顯差距
```

### AlphaFold2 的技術架構

AlphaFold2 採用了創新的架構：

```python
# AlphaFold2 核心概念

"""
1. Evoformer Block：
   - 多序列對齊（MSA）
   - 配對關係建模
   - 注意力機制

2. 結構模組：
   - 從隱表示生成 3D 座標
   - 不動點迭代（iterative refinement）
   - 旋轉和平移的表示學習
"""

# 簡化示意
class AlphaFold2:
    def predict(self, sequence):
        # 1. 特徵提取
        msa = self.build_msa(sequence)
        pair_repr = self.pair_sequences(sequence)
        
        # 2. Evoformer 處理
        for layer in range(48):
            msa, pair_repr = self.evoformer_block(msa, pair_repr)
        
        # 3. 結構生成
        structure = self.structure_module(msa, pair_repr)
        
        return structure
```

### 關鍵創新

```
AlphaFold2 技術亮點：
────────────────────────────────

1. 注意力機制的應用
   - 學習胺基酸之間的長距離交互
   - 捕捉進化關係

2. 端到端學習
   - 直接預測 3D 座標
   - 無需中間步驟

3. 訓練目標
   - 結構幾何約束
   - 物理可行性約束

4. 置信度預測
   - pLDDT 分數
   - 預測每個殘基的可靠性
```

## 對科學的影響

### 藥物開發

```
傳統藥物開發：
研究新藥 → 平均 10-15 年 → 費用數十億美元
    │
    ├── 辨識疾病相關蛋白質 ──► 慢
    ├── 確定蛋白質結構 ─────► 更慢
    └── 基於結構設計藥物 ───► 需要精確結構

AlphaFold2 之後：
研究新藥 → 更快
    │
    ├── 直接預測蛋白質結構
    ├── 快速篩選藥物靶點
    └── 加速藥物設計
```

### 基礎研究

```
蛋白質結構資料庫：
────────────────────────────────

PDB（蛋白質資料庫）：~170,000 結構（2020年）

AlphaFold DB（2021年上線）：
  - 人類蛋白質組：~20,000 蛋白質
  - 總計數百萬結構
  - 全部公開免費

影響：大幅加速蛋白質功能研究
```

## AlphaFold2 的開放

### 開源和資料庫

DeepMind 選擇了有限度的開放：

```
AlphaFold2 開放狀態：
────────────────────────────────

2021 年：
- AlphaFold Server：開放研究使用
- AlphaFold DB：人類蛋白質組開放
- AlphaFold2 論文：完整技術細節
- 部分代碼：開源

未完全開源：
- 完整訓練流程
- 某些推斷細節
```

### 使用 AlphaFold

```python
# AlphaFold2 預測流程（概念）

from alphafold import AlphaFold

# 輸入：蛋白質序列
sequence = "MKTAYIAKQRQISFVKSHFSRQLEERLGLIEVQAPILSRVGDGTQDNLSGAEKEK" * 10

# 預測
model = AlphaFold(model_name="model_1")
structure = model.predict(sequence)

# 輸出：3D 結構（PDB 格式）
# 置信度：pLDDT 分數
```

## 後續發展

### AlphaFold-Multimer

支援蛋白質複合體預測：

```python
# 蛋白質複合體預測
complex_structure = model.predict_multimer(
    chain_A_sequence,
    chain_B_sequence
)
```

### RoseTTAFold 和其他模型

AlphaFold2 之後，其他團隊也快速跟進：

```
其他蛋白質結構預測模型：
────────────────────────────────

RoseTTAFold (Baker Lab):
  - 2021 年發布
  - 開源
  - 較低的計算需求

ESMFold (Meta AI):
  - 2022 年發布
  - 完全基於語言模型
  - 預測速度更快

DeepMind AlphaFold2:
  - 持續更新
  - AlphaFold Server 持續開放
```

## 延伸閱讀

- [AlphaFold2 論文](https://www.google.com/search?q=AlphaFold2+Nature+paper+protein+structure)
- [DeepMind AlphaFold 頁面](https://www.google.com/search?q=DeepMind+AlphaFold+protein+folding)
- [CASP14 競賽結果](https://www.google.com/search?q=CASP14+protein+structure+prediction+results)
- [AlphaFold 資料庫](https://www.google.com/search?q=AlphaFold+protein+structure+database)

---

*本篇文章為「AI 程式人雜誌 2020 年 10 月號」文章集錦之一。*

（編者註：AlphaFold2 的 CASP14 結果實際於 2020 年 11 月公布，請參考 2020 年 11 月號的更詳細報導。）