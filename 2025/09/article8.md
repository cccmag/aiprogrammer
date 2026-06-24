# 程式碼覆蓋率

## 前言

程式碼覆蓋率（Code Coverage）是衡量測試品質的常用指標之一。它告訴你：「在執行測試的過程中，有多少百分比的程式碼被執行到了？」雖然高覆蓋率不代表測試品質好，但低覆蓋率幾乎總是代表測試不足。

## 覆蓋率的類型

覆蓋率有多種測量維度：

### 行覆蓋率（Line Coverage）

最基本的覆蓋率——程式碼中有多少「行」被執行過了。

```python
def calculate(a, b):    # 第 1 行
    if a > 0:           # 第 2 行
        return a + b    # 第 3 行（如果 a > 0 才會執行）
    return a - b        # 第 4 行（如果 a <= 0 才會執行）
```

如果測試只測試了 `a > 0` 的情況，行覆蓋率是 75%（第 1、2、3 行被執行，第 4 行未執行）。

### 分支覆蓋率（Branch Coverage）

追蹤每個條件分支（if/else、case/match）是否都被執行過。上面的例子中，分支覆蓋率是 50%（只有 `a > 0` 的分支被測試，`a <= 0` 的分支沒有）。

### 條件覆蓋率（Condition Coverage）

對於複合條件（如 `a > 0 and b < 10`），追蹤每個子條件的 True/False 是否都被測試過。

### 路徑覆蓋率（Path Coverage）

追蹤所有可能的執行路徑。這是最嚴格的覆蓋率標準，但對複雜函數來說可能不切實際——路徑數量可能隨條件數量指數成長。

## 使用 Coverage.py

Python 最流行的覆蓋率工具是 `coverage.py`。

### 安裝

```bash
pip install coverage
```

### 基本使用

```bash
# 執行測試並收集覆蓋率
coverage run -m pytest tests/

# 產生報表
coverage report

# 產生 HTML 報表（可互動瀏覽）
coverage html
```

### 輸出範例

```
Name                     Stmts   Miss  Cover
--------------------------------------------
src/calculator.py           20      2    90%
src/utils.py                15      5    67%
src/database.py             30     10    67%
--------------------------------------------
TOTAL                       65     17    74%
```

### 設定檔案

```ini
# .coveragerc
[run]
source = src/
omit = */tests/*

[report]
exclude_lines =
    pragma: no cover
    def __repr__
    raise NotImplementedError
```

## 與 pytest 整合

```bash
pip install pytest-cov
```

```bash
pytest tests/ --cov=src --cov-report=html --cov-report=term
```

在 `pytest.ini` 中設定：

```ini
[pytest]
addopts = --cov=src --cov-report=term-missing --cov-fail-under=80
```

## 解讀覆蓋率報表

### 應該關注什麼？

**未覆蓋的行**：報表中的 `Missing` 欄位會列出未執行的行號。檢查這些行是否是遺漏的測試案例。

**分支覆蓋率**：行覆蓋率 100% 不等於分支覆蓋率 100%。如果一行中有 `if a or b`，行覆蓋率只要這行被執行就算 100%，但分支覆蓋率要求 `a=True`、`a=False`、`b=True`、`b=False` 都要被覆蓋。

### 覆蓋率的陷阱

**高覆蓋率 ≠ 高品質**：你可以寫一個測試只呼叫了函數但沒有做任何斷言，覆蓋率報表會顯示這行程式碼「被覆蓋」，但實際上你並沒有驗證任何行為。

**100% 覆蓋率不切實際**：追求 100% 覆蓋率通常導致邊際效益遞減。最後 10% 的覆蓋率可能需要花費與前 90% 相同的努力。實務上 80-90% 是合理的目標。

**忽略異常處理路徑**：錯誤處理程式碼在正常情況下不會被執行，但這些路徑恰恰是最需要測試的——因為它們在上線後最可能出錯。

## 覆蓋率門檻（Quality Gate）

在 CI 中設定覆蓋率門檻是一個常見實踐：

```yaml
# GitHub Actions
- name: Coverage check
  run: |
    pytest --cov=src --cov-fail-under=80
```

當覆蓋率低於門檻時，CI 會失敗，防止低覆蓋率的程式碼合併到主分支。

## 覆蓋率的最佳實踐

**目標導向**：根據專案特性設定合理的覆蓋率目標。核心業務邏輯要高覆蓋率（90%+），工具類別可以適度放寬。

**重點關注分支覆蓋率**：行覆蓋率容易達成，但分支覆蓋率更能反映測試的完整性。

**不要為覆蓋率寫測試**：測試的目的是驗證行為的正確性，而不是提高覆蓋率數字。

**定期審查覆蓋率趨勢**：關注覆蓋率的變化趨勢，而不是絕對值。如果覆蓋率突然下降，這可能是一個危險信號。

## 小結

覆蓋率是一個有用的指標，但它只是測試品質的「代理指標」——它告訴你「有多少程式碼被測試執行過」，但不告訴你「測試是否驗證了正確的行為」。好的測試策略是：**用覆蓋率發現未測試的程式碼，用人腦判斷這些測試是否足夠**。

## 延伸閱讀

- [Coverage.py 官方文件](https://www.google.com/search?q=coverage+py+documentation)
- [pytest-cov 使用指南](https://www.google.com/search?q=pytest+cov+usage)
- [覆蓋率的陷阱與最佳實踐](https://www.google.com/search?q=code+coverage+pitfalls+best+practices)
