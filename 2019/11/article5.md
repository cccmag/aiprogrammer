# Kubernetes 1.17：儲存與網路的改進

## 前言

Kubernetes 1.17 於 2019 年 12 月發布，這是 2019 年的最後一個版本。本篇文章將介紹 K8s 1.17 的重要更新。

## Kubernetes 1.17 的重要更新

### Cloud Provider Labels 升級

K8s 1.17 將 Cloud Provider Labels 升級為 Beta 並預設啟用：

```yaml
# 新的標籤格式
topology.kubernetes.io/region: us-east-1
topology.kubernetes.io/zone: us-east-1a
```

### CSI Migration

Container Storage Interface (CSI) Migration 繼續完善：

```
CSI Migration 的目標：
- 將 in-tree 儲存外掛遷移到 CSI
- 統一的儲存介面
- 減少對雲端供應商的依賴
```

### 節點暫時存儲管理

K8s 1.17 加強了對節點暫時存儲的管理：

```yaml
# 新增的 Ephemeral Storage 管理
apiVersion: v1
kind: Pod
spec:
  containers:
    - name: app
      resources:
        limits:
          ephemeral-storage: 2Gi
```

## Kubernetes 的持續演進

### 版本發布節奏

Kubernetes 保持每年四個版本的發布節奏：

```
2019 年：
- 1.15：增強可扩展性
- 1.16：Custom Resources 穩定化
- 1.17：儲存和網路改進
```

### 社群活躍度

Kubernetes 是迄今為止最活躍的開源專案之一：

```
統計：
- GitHub stars：超過 70,000
- 貢獻者：超過 2,000 人
- 生態系統：不斷擴大
```

## 結論

Kubernetes 1.17 延續了 K8s 的持續改進策略。隨著 Kubernetes 的成熟，它已經成為容器編排的事實標準。建議開發者和運維團隊持續關注 K8s 的發展，並規劃升級路徑。

---

**延伸閱讀**

- [Kubernetes+1.17+release+notes](https://www.google.com/search?q=Kubernetes+1.17+release+notes)
- [Kubernetes+CSI+Migration](https://www.google.com/search?q=Kubernetes+CSI+migration)
- [Kubernetes+storage](https://www.google.com/search?q=Kubernetes+storage+2019)