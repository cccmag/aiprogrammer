# 資料治理與隱私：AI 時代的資料生命週期管理

## 前言

資料是 AI 的燃料，但未經妥善治理的資料可能帶來法律風險和模型偏見。GDPR、CCPA 等法規要求企業對資料的收集、儲存、處理和刪除進行全生命週期管理。

## 匿名化處理與差分隱私

```python
import pandas as pd
import numpy as np

class DataAnonymizer:
    def __init__(self, epsilon: float = 1.0):
        self.epsilon = epsilon

    def k_anonymize(self, df: pd.DataFrame, quasi_identifiers: list, k: int = 5):
        return df.groupby(quasi_identifiers).filter(lambda x: len(x) >= k)

    def add_laplace_noise(self, value: float, sensitivity: float = 1.0):
        scale = sensitivity / self.epsilon
        noise = np.random.laplace(0, scale)
        return value + noise

    def generalize_age(self, age: int) -> str:
        bins = [(0, 18), (18, 30), (30, 50), (50, 999)]
        for low, high in bins:
            if low <= age < high:
                return f"{low}-{high-1}"

anon = DataAnonymizer(epsilon=0.5)
data = pd.DataFrame({
    'name': ['Alice', 'Bob', 'Charlie'],
    'age': [28, 35, 42],
    'zip': ['10001', '10002', '10003'],
    'income': [50000, 60000, 70000]
})

data['age'] = data['age'].apply(anon.generalize_age)
data['income'] = data['income'].apply(
    lambda x: anon.add_laplace_noise(x, sensitivity=10000)
)
print(data.drop(columns=['name']))
```

## 資料最小化原則的實作

```python
class DataMinimizer:
    REQUIRED_FIELDS = {'email', 'age_range'}
    OPTIONAL_FIELDS = {'preferences', 'location_city'}

    def minimize(self, raw_data: dict) -> dict:
        minimal = {}
        for field in self.REQUIRED_FIELDS:
            if field in raw_data:
                minimal[field] = raw_data[field]
        return minimal

minimizer = DataMinimizer()
user_data = {
    'email': 'alice@example.com',
    'password': 'secret123',
    'ip_address': '192.168.1.1',
    'browser_fingerprint': 'abc123'
}
print(minimizer.minimize(user_data))
```

## 結語

資料治理需要技術與政策的雙重保障。建議建立資料分類制度、實施最小權限原則，並定期進行資料保護衝擊評估（DPIA）。

---

**延伸閱讀**

- [GDPR 資料保護原則](https://www.google.com/search?q=GDPR+data+protection+principles+minimization)
- [差分隱私介紹](https://www.google.com/search?q=differential+privacy+explanation+Python)
- [k-匿名化技術](https://www.google.com/search?q=k+anonymity+privacy+preserving+data+publishing)
