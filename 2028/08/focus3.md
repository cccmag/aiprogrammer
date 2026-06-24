# 資料漂移與概念漂移檢測

## 統計檢定到自動化檢測（2019-2028）

### 前言

模型上線後的最大挑戰不是程式錯誤，而是資料變了。顧客行為改變、季節因素、新產品上架——這些都會導致模型表現退化。資料漂移（Data Drift）和概念漂移（Concept Drift）是兩類最常見的變遷。

### 資料漂移 vs. 概念漂移

**資料漂移**：輸入特徵的分佈改變了，但輸入到輸出的映射關係不變。

例如：使用者年齡從 25-35 變成 40-55，但模型對每個年齡的預測仍然是正確的。

**概念漂移**：輸入到輸出的映射關係改變了，但輸入分佈不變。

例如：COVID-19 改變了「發燒 + 咳嗽」與「就醫意願」之間的關係，但症狀本身的分佈不變。

### 常見檢測方法

**1. 統計檢定**

| 方法 | 適用 | 說明 |
|------|------|------|
| KS 檢定 | 連續特徵 | 比較參考分佈與當前分佈 |
| Chi-Square | 類別特徵 | 比較類別頻率變化 |
| PSI（Population Stability Index） | 通用 | 衡量分佈偏移程度 |

```python
# PSI 計算範例
import numpy as np

def psi(expected, actual, buckets=10):
    eps = 1e-6
    expected_pct = np.histogram(expected, bins=buckets)[0] / len(expected) + eps
    actual_pct = np.histogram(actual, bins=buckets)[0] / len(actual) + eps
    return np.sum((actual_pct - expected_pct) * np.log(actual_pct / expected_pct))
```

**2. 特徵層級漂移**

針對每個特徵單獨計算漂移分數。聚焦在最重要的前 N 個特徵，避免「警報疲勞」。

**3. 模型層級漂移**

監控模型輸出的分佈變化。如果預測類別的分佈突然改變，即使準確率還未下降，也是重要警訊。

### 偵測架構

```
參考視窗（Reference Window）
       │
       ▼
┌──────────────┐    ┌──────────────┐
│  推論請求     │───▶│  特徵提取     │
└──────────────┘    └──────┬───────┘
                           ▼
                    ┌──────────────┐
                    │  漂移檢測引擎  │◀── 統計檢定
                    └──────┬───────┘    │
                           ▼            │
                    ┌──────────────┐    │
                    │  Drift Report │    │
                    └──────┬───────┘    │
                           ▼            │
                    ┌──────────────┐    │
                    │  警報系統     │────┘
                    └──────────────┘
```

### 實務陷阱

1. **多重比較問題**：監控 100 個特徵時，即使沒有漂移，也有約 5 個特徵會因為隨機因素被誤判。使用 Bonferroni 校正或 FDR 控制。
2. **季節性**：週末與平日資料分佈天然不同。使用同期的參考視窗。
3. **回饋延遲**：Ground truth 可能數小時甚至數天後才到達。在這期間，需要使用代理指標。

### 工具對照

| 工具 | 漂移檢測方法 | 整合方式 |
|------|-------------|----------|
| Evidently | PSI, KS, Chi-Square | Python Library |
| WhyLabs | 基於分佈距離 | SaaS API |
| Alibi Detect | ADWIN, Kolmogorov-Smirnov | Python Library |
| NannyML | 基於置信度 | Python Library |

### 小結

漂移檢測不是一次性的設定，而是持續優化的過程。閾值調太緊會警報疲勞、調太鬆會錯過真實問題。定期回顧 Drift Report 並調整檢測策略，是 MLOps 團隊的重要工作。

---

**下一步**：[推論日誌與分散式追蹤](focus4.md)

## 延伸閱讀

- [Evidently Drift Detection](https://www.google.com/search?q=Evidently+drift+detection+PSI)
- [Alibi Detect Library](https://www.google.com/search?q=Alibi+Detect+drift+detection)
- [Concept Drift Survey](https://www.google.com/search?q=concept+drift+detection+survey+2024)
