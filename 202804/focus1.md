# AI 資料工程導論（2016-2028）

## 從資料庫到資料湖

2016 年，Google 發表了《Hidden Technical Debt in Machine Learning Systems》，首次系統性地指出 ML 系統中資料管線的技術債遠超模型代碼。這篇論文點醒了整個產業：**資料不是副產品，資料是產品本身。**

```
2010s 早期：關聯式資料庫 → ETL → 靜態報表
2016s 轉折：資料湖（Data Lake）→ ELT → ML 管線
2020s 現在：特徵平台 + 資料版本控制 + 品質監控
```

這十年間，資料基礎設施經歷了三波演進。第一波是 Hadoop 生態系（2008-2015），以 HDFS 和 MapReduce 為核心。第二波是雲端資料倉儲（2015-2020），Snowflake 和 BigQuery 重新定義了資料儲存與查詢。第三波（2020-2028）則是 AI 原生資料工程，重點從「儲存資料」轉向「服務模型」。

## 資料工程的四個層次

```
┌─────────────────────────────────────────┐
│  4. Consumption Layer                    │
│     特徵服務、模型推論、即時查詢         │
├─────────────────────────────────────────┤
│  3. Quality Layer                        │
│     資料驗證、異常檢測、血緣追蹤         │
├─────────────────────────────────────────┤
│  2. Storage Layer                        │
│     特徵儲存、資料版本、中繼資料管理     │
├─────────────────────────────────────────┤
│  1. Pipeline Layer                       │
│     資料攝取、轉換、編排、排程           │
└─────────────────────────────────────────┘
```

## 為什麼現在是資料工程？

AI 模型架構趨向成熟（Transformer、Diffusion），但資料品質差異才是決定模型效能的關鍵。Andrew Ng 在 2021 年提出了「以資料為中心的 AI」（Data-Centric AI），強調與其優化模型架構不如優化資料品質。

### 資料工程 vs. 傳統後端

| 面向 | 後端工程 | 資料工程 |
|------|---------|---------|
| 資料量 | MB-GB 級 | GB-PB 級 |
| 時效性 | 即時交易 | 批次+即時 |
| 正確性 | 強一致性 | 最終一致性 |
| 測試 | 單元/整合測試 | 資料驗證+監控 |

## Python 範例：簡單的資料管線

```python
import pandas as pd

def etl_pipeline(raw_path: str, output_path: str):
    df = pd.read_csv(raw_path)
    df = df.dropna(subset=["id", "timestamp"])
    df["date"] = pd.to_datetime(df["timestamp"]).dt.date
    df["features"] = df.groupby("user_id")["amount"].transform("mean")
    df.to_parquet(output_path, index=False)
```

## 關鍵里程碑

- **2016**：Google ML Tech Debt 論文
- **2018**：DVC 開源資料版本控制
- **2019**：Feast 開源特徵儲存
- **2020**：Great Expectations 資料品質框架
- **2023**：LakeFS GA 資料湖版本控制
- **2025**：資料工程平台趨向標準化

## 延伸閱讀

- [Google Hidden Technical Debt in ML Systems](https://www.google.com/search?q=Hidden+Technical+Debt+in+Machine+Learning+Systems+2016)
- [Data-Centric AI Andrew Ng](https://www.google.com/search?q=Data+Centric+AI+Andrew+Ng+2021)
- [What is a Data Lake](https://www.google.com/search?q=data+lake+architecture+guide)

---

*本篇文章為「AI 程式人雜誌 2028 年 4 月號」資料工程系列之一。*
