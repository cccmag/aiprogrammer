# Python 年度報告

## 生態概況

2025 年 Python 在 TIOBE 指數維持 15.8% 的領先地位，PyPI 套件總數突破 60 萬。Python 3.14 於 2025 年 10 月發布，帶來了多項重大改進。

## Python 3.14 新功能

### 模式匹配強化

```python
def process_command(command):
    match command.split():
        case ["quit"]:
            return "Goodbye!"
        case ["hello", name]:
            return f"Hello, {name}!"
        case ["add", *nums]:
            return sum(int(n) for n in nums)
        case _:
            return "Unknown command"
```

### 更快的 CPython

3.14 引入了新的 JIT 編譯器（基於 copy-and-patch 技術），在數值運算與迴圈密集的場景中獲得 30-60% 的效能提升。

```python
# JIT 自動加速數值計算
def compute_pi(n):
    total = 0.0
    for k in range(n):
        total += (4.0 / (8*k + 1) - 2.0 / (8*k + 4)
                  - 1.0 / (8*k + 5) - 1.0 / (8*k + 6)) / 16**k
    return total
```

## 關鍵趨勢

### Mojo 相容層

Mojo 推出了 Python 相容模式，可直接執行 Python 程式碼並自動加速。這讓 Python 開發者可以逐步遷移到更高性能的執行環境。

### PyPI 安全升級

2025 年 PyPI 強制所有維護者啟用 2FA，並導入 Sigstore 套件簽署機制。下載量前 1% 的套件需要通過額外的安全審查。

### 資料生態系鞏固

Polars 在 2025 年超越 Pandas 成為 DataFrame 首選。Polars 的惰性求值與多線程引擎在大型資料集上比 Pandas 快 5-20 倍。

```python
import polars as pl

df = pl.read_csv("large_dataset.csv")
result = (
    df
    .filter(pl.col("sales") > 1000)
    .group_by("category")
    .agg(pl.col("amount").sum().alias("total"))
    .sort("total", descending=True)
)
```

## 參考資料

- [Google 搜尋：Python 3.14 new features](https://www.google.com/search?q=Python+3.14+new+features+2025)
- [Google 搜尋：Polars vs Pandas 2025](https://www.google.com/search?q=Polars+vs+Pandas+2025+performance)
- [Google 搜尋：PyPI 2FA 2025](https://www.google.com/search?q=PyPI+mandatory+2FA+2025)
