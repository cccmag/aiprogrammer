# 測試覆蓋率與品質指標（2014-2016）

## 前言

測試覆蓋率是衡量測試完整性的指標，但不應成為追逐的目標。了解覆蓋率的同時，更要關注有意義的品質指標。

## 覆蓋率類型

| 類型 | 說明 | 目標 |
|------|------|------|
| **函數覆蓋** | 多少函數被調用 | > 80% |
| **行覆蓋** | 多少程式行被執行 | > 70% |
| **分支覆蓋** | 多少條件分支被測試 | > 60% |
| **路徑覆蓋** | 多少執行路徑被涵蓋 | 難達到 100% |

## Python 覆蓋率工具

```bash
pip install pytest-cov
pytest --cov=myapp --cov-report=html tests/
```

```python
# conftest.py
import pytest

def pytest_configure(config):
    config.addinivalue_line(
        "markers", "slow: marks tests as slow"
    )
```

## JavaScript 覆蓋率工具

```bash
npm install --save-dev jest
jest --coverage
```

```javascript
// jest.config.js
module.exports = {
  coverageDirectory: 'coverage',
  collectCoverageFrom: [
    'src/**/*.js',
    '!src/**/*.test.js'
  ],
  coverageThreshold: {
    global: {
      branches: 50,
      functions: 50,
      lines: 50,
      statements: 50
    }
  }
};
```

## Codecov 整合

```yaml
# .travis.yml
language: node_js
after_success:
  - bash <(curl -s https://codecov.io/bash)
```

## 品質指標儀表板

```python
# quality_dashboard.py
from dataclasses import dataclass
from typing import List

@dataclass
class QualityMetrics:
    coverage: float
    bugs: int
    vulnerabilities: int
    code_smells: int
    
    @property
    def quality_score(self) -> float:
        score = self.coverage
        score -= self.bugs * 2
        score -= self.vulnerabilities * 5
        score -= self.code_smells * 0.5
        return max(0, min(100, score))

class Dashboard:
    def __init__(self):
        self.metrics_history: List[QualityMetrics] = []
    
    def add_metrics(self, metrics: QualityMetrics):
        self.metrics_history.append(metrics)
    
    def get_trend(self) -> str:
        if len(self.metrics_history) < 2:
            return "insufficient data"
        latest = self.metrics_history[-1]
        previous = self.metrics_history[-2]
        diff = latest.quality_score - previous.quality_score
        if diff > 0:
            return f"+{diff:.1f} improvement"
        return f"{diff:.1f} regression"
```

## 測試品質判斷

### 好的測試

```python
def test_calculate_total_with_valid_items():
    """測試邏輯清晰的正常路徑"""
    items = [{"price": 10}, {"price": 20}]
    assert calculate_total(items) == 30
```

### 壞的測試（過度 mock）

```python
def test_calculate_total_mocked():
    """過度使用 mock，測試變得無意義"""
    calc = Mock()
    calc.calculate_total.return_value = 30
    assert calc.calculate_total([...]) == 30  # 只測 mock
```

## 報表中常見問題

```bash
# 檢視低覆蓋率的檔案
pytest --cov=myapp --cov-report=term-missing tests/
```

## 相關資源

- [測試覆蓋率工具](https://www.google.com/search?q=code+coverage+tools+2016)
- [Codecov 服務](https://www.google.com/search?q=codecov+code+coverage)
- [軟體品質指標](https://www.google.com/search?q=software+quality+metrics+2016)

## 結語

覆蓋率是參考指標，不是目標。專注於有意義的測試案例，確保關鍵路徑被完整測試，比追求高覆蓋率數字更重要。

---

*本篇文章為「AI 程式人雜誌 2016 年 10 月號」軟體測試系列之一。*