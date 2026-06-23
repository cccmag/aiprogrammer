# AI 系統健康檢查框架

## 被動監控到主動檢查（2024-2028）

### 前言

健康檢查（Health Check）與監控不同：監控是持續觀察，健康檢查是定期測試。一個完善的健康檢查框架能確保 AI 系統的所有元件在部署前和運行中都符合預期。

### 健康檢查的層次

```
L1: 基礎存活檢查
   └── 模型服務是否有回應？
L2: 依賴服務檢查
   └── 資料庫、快取、特徵儲存是否連得上？
L3: 模型功能檢查
   └── 模型是否回傳非空且格式正確的結果？
L4: 品質檢查
   └── 模型的準確率是否在可接受範圍？
L5: 端到端演練
   └── 模擬真實請求，驗證完整流程？
```

### 實作健康檢查

`_code/observability.py` 中的 `HealthChecker` 類別展示了輕量級的實作：

```python
hc = HealthChecker()
hc.register("model_loaded", lambda: model is not None)
hc.register("database_up", lambda: db.ping())
hc.register("cache_warm", lambda: cache.hit_rate() > 0.8)
status = hc.run_all()
# Status: healthy / degraded / down
```

### 啟動檢查 vs. 運行時檢查

**啟動檢查（Startup Probe）**：模型容器啟動時，確認所有依賴已就緒。失敗則不註冊到服務發現。

**存活檢查（Liveness Probe）**：運行中定期確認。如果模型處理序死鎖，Kubernetes 會自動重啟 Pod。

**就緒檢查（Readiness Probe）**：確認可以接受流量。快取還沒預熱完成時，暫時不接收請求。

### 檢查項目的設計原則

| 原則 | 說明 |
|------|------|
| 快速 | 每個檢查應在 100ms 內完成 |
| 獨立 | 檢查之間不互相依賴 |
| 確定性 | 同樣條件下結果一致 |
| 安全 | 不修改系統狀態（唯讀） |

### 健康評分與健康路由

健康檢查結果可以聚合為單一健康分數，用於流量路由：

- **Healthy（0 失敗）**：正常接收流量
- **Degraded（< 1/3 失敗）**：仍接收流量，但監控標記
- **Down（≥ 1/3 失敗）**：從負載均衡器中移除

### 與 Kubernetes 整合

```yaml
livenessProbe:
  httpGet:
    path: /health/live
    port: 8080
  initialDelaySeconds: 30
  periodSeconds: 10
readinessProbe:
  httpGet:
    path: /health/ready
    port: 8080
  initialDelaySeconds: 5
  periodSeconds: 5
```

### 模型層級的健康檢查

除了一般服務健康檢查，AI 系統還需要模型專屬的檢查：
1. **模型簽章驗證**：確認模型的輸入輸出 schema 未變
2. **推理測試**：用測試樣本執行推理，驗證結果合理性
3. **資源檢查**：GPU 是否存在、VRAM 是否足夠

### 小結

健康檢查是 AI 系統可靠性的第一道防線。它不應該等到系統異常才執行——在 CI/CD 管線中、在部署前、在流量切換時，都應該執行針對性的健康檢查。

---

**下一步**：[可觀測性工具生態](focus7.md)

## 延伸閱讀

- [Kubernetes Probe Guide](https://www.google.com/search?q=Kubernetes+liveness+readiness+probe+ML)
- [ML System Health Check](https://www.google.com/search?q=ML+system+health+check+best+practices)
- [Health Check Patterns](https://www.google.com/search?q=health+check+pattern+microservices)
