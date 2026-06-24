# 程式碼解析：年度回顧資料分析

## 概覽

`_code/year_review.py` 是一個年度數據回顧工具，示範如何用 Python 處理程式語言趨勢與 AI 工具採用率的數據分析。

## 核心功能

### 1. 數據生成

```python
def generate_language_data():
    """Generate programming language trend data for 2025."""
    languages = {
        "Python":      {"tiobe": 15.8, "github_repos": 8500000,  "growth": 12.5, "jobs": 42000},
        "JavaScript":  {"tiobe": 8.2,  "github_repos": 12000000, "growth": 3.2,  "jobs": 38000},
        "TypeScript":  {"tiobe": 6.5,  "github_repos": 5200000,  "growth": 18.7, "jobs": 28000},
    ...
```

使用字典結構儲存多維數據，每種語言包含 TIOBE 指數、GitHub 倉庫數、年成長率與職缺數。

### 2. 綜合評分演算法

```python
def compute_trends(languages):
    scores = {}
    for name, data in languages.items():
        scores[name] = (
            data["tiobe"] * 0.3
            + data["growth"] * 0.4
            + math.log10(data["github_repos"] + 1) * 0.3
        )
```

加權評分公式：TIOBE 指數 30%、成長率 40%、生態規模 30%。`log10` 處理 GitHub 倉庫數量級差異。

### 3. 視覺化報表

```python
def generate_report(languages, tools, trends):
    for i, (name, data) in enumerate(trends["by_tiobe"], 1):
        bar = "█" * max(1, int(data["tiobe"] / 1.5))
        lines.append(f"  {i}. {name:12s} {data['tiobe']:5.1f}% {bar}")
```

使用 Unicode 區塊字符製作簡易條形圖，直接輸出終端機即可閱讀。

## 執行方式

```bash
cd _code
bash test.sh
# 或直接執行
python3 year_review.py
```

## 參考資料

- [Google 搜尋：Python data analysis](https://www.google.com/search?q=Python+data+analysis+tutorial)
- [Google 搜尋：Unicode block characters terminal](https://www.google.com/search?q=unicode+block+characters+terminal+python)
