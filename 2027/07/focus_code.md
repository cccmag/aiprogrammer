# 程式實作：Mini MLOps 平台

## 簡介

本實作展示 MLOps/LLMOps 的核心元件：提示詞版本管理、A/B 測試、漂移偵測、效能監控、LLM 評估。完整程式碼在 `_code/mlops.py`。

## 核心元件

### 1. 提示詞版本管理

提示詞像程式碼一樣需要版本控制：

```python
class PromptRegistry:
    def register(self, prompt: PromptTemplate): ...
    def get_latest(self, name: str) -> PromptTemplate: ...
    def rollback(self, name: str, version: str) -> PromptTemplate: ...
    def list_versions(self, name: str) -> list[str]: ...
```

支援建立、查詢、回滾操作，每次變更都記錄版本號與時間戳。

### 2. A/B 測試

比較不同提示詞版本的實際表現：

```python
class ABTest:
    def select_variant(self) -> str:
        # 根據流量分配比例選擇版本
    def record_metric(self, variant: str, value: float):
        # 記錄使用者回饋分數
    def report(self) -> dict:
        # 計算統計顯著性 (t-test)
```

### 3. 漂移偵測

使用 Population Stability Index (PSI) 檢測資料分布變化：

```python
def psi_score(reference, current, bins=10) -> float:
    """PSI > 0.2 表示顯著漂移"""
    psi = sum((p_i - q_i) * log(p_i / q_i) for ...)
    return psi

class DriftMonitor:
    def check_drift(self, current_values) -> dict:
        psi = psi_score(self.reference, current_values)
        return {"drifted": psi > self.threshold, "psi": psi}
```

### 4. 效能監控

追蹤模型服務的關鍵指標：

```python
class ModelPerformanceMonitor:
    def record_request(self, latency_ms, success): ...
    def report(self):
        return {
            "error_rate": ...,
            "latency_ms_p50": ...,
            "latency_ms_p99": ...,
            "avg_throughput_rps": ...,
        }
```

### 5. LLM 評估

使用 LLM-as-Judge 模式評估生成品質：

```python
def llm_as_judge_score(response: str, rubric: dict) -> float:
    """根據評估標準給分（長度、代碼、解釋、範例）"""
```

## 執行結果

```
--- A/B Test Results ---
v1: mean=0.496, n=59
v2: mean=0.655, n=41
Statistically significant: True

--- Drift Detection ---
PSI: 2.44 (threshold: 0.2)
Drift detected: True

--- Model Performance ---
Error rate: 1.00%
Latency P50: 151.86ms
Latency P99: 267.46ms
```

## 執行方式

```bash
cd _code
python3 mlops.py
```

## 延伸練習

1. **加入真實監控後端**：將指標寫入 Prometheus + Grafana
2. **提示詞測試**：實作提示詞的自動化測試（單元測試、回歸測試）
3. **串接 LLM API**：使用 OpenAI/Claude API 進行真實 A/B 測試
4. **自動 Rollback**：當漂移或錯誤率超標時自動回滾模型或提示詞
5. **儀表板**：使用 Streamlit 建立 MLOps 視覺化儀表板
