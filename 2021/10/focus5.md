# 測試覆蓋率與程式碼品質

## 覆蓋率的概念

測試覆蓋率衡量測試套件對程式碼的覆蓋程度。高覆蓋率表示更多程式碼被執行過，但不直接代表測試品質。100% 覆蓋率不等於沒有 bug，但覆蓋率過低通常表示測試不足。

## Coverage.py 使用

```bash
pip install coverage
coverage run -m pytest
coverage report
coverage html
```

Coverage.py 會追蹤哪些程式碼行被執行，並產生詳細報告。

## 分支覆蓋率

除了行覆蓋率，分支覆蓋率更重要：

```python
# 這段程式碼有兩個分支
if condition:
    do_something()
else:
    do_other()
```

分支覆蓋率衡量每個分支是否都被測試過：

```bash
coverage run --branch -m pytest
coverage report
```

## 解讀覆蓋率報告

```
Name                      Stmts   Miss  Cover
---------------------------------------------
my_module.py                 50      5    90%
my_package/
    __init__.py              10      0   100%
    core.py                  100     20    80%
```

忽略特定程式碼：

```python
if __debug__:
    # 這行不需要測試
    run_development_checks()  # pragma: no cover
```

## 覆蓋率與測試品質

覆蓋率是工具，不是目標。刻意提高覆蓋率可能導致無意義的測試。有效的策略是：

- 聚焦關鍵路徑和業務邏輯
- 優先測試複雜、有風控的程式碼
- 使用分支覆蓋率發現未測試的分支

## 程式碼複雜度分析

結合覆蓋率和複雜度分析：

```bash
pip install radon
radon cc -a my_module.py
```

複雜度高的函式（圈複雜度 > 10）需要更多測試關注。

## CI 中的覆蓋率追蹤

在 CI 中記錄覆蓋率趨勢，可以發現測試退化的早期信號：

```yaml
# GitHub Actions
- name: Run tests with coverage
  run: coverage run -m pytest && coverage xml
- name: Upload coverage
  uses: codecov/codecov-action@v2
```

Codecov、Coveralls 等服務可以追蹤覆蓋率變化並發出警告。

## 結論

覆蓋率是衡量測試完整性的有用指標，但要與測試品質、其他品質工具（如 linter、類型檢查）結合使用，才能建立全面的品質保障體系。