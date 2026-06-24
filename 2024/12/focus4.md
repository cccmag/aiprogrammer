# Focus 4：雲端與 DevOps 演進

## AI 驅動維運

2024 年雲端維運最大的變化是 AI 的深度整合。從異常檢測到根因分析，AI 已成為 SRE 團隊的核心工具。

```javascript
// 模擬 AI 驅動的異常檢測系統
class AnomalyDetector {
  constructor(threshold = 2.5) {
    this.threshold = threshold;
    this.metrics = [];
  }

  collect(latency, errorRate, cpuUsage) {
    this.metrics.push({ latency, errorRate, cpuUsage });
  }

  detect() {
    const avg = this.metrics.reduce((a, b) => ({
      latency: a.latency + b.latency / this.metrics.length,
      errorRate: a.errorRate + b.errorRate / this.metrics.length,
      cpuUsage: a.cpuUsage + b.cpuUsage / this.metrics.length
    }), { latency: 0, errorRate: 0, cpuUsage: 0 });

    const latest = this.metrics[this.metrics.length - 1];
    const score = Math.abs(latest.latency - avg.latency) / avg.latency;
    return score > this.threshold ? 'Anomaly detected' : 'Normal';
  }
}

const detector = new AnomalyDetector();
detector.collect(120, 0.01, 55);
detector.collect(125, 0.02, 60);
detector.collect(450, 0.15, 90); // 異常
console.log(detector.detect());
```

## Serverless 持續進化

AWS Lambda 新增 VPC 改善、Cloudflare Workers 支援 Python、Deno Deploy 穩定成長。

## 容器與調度

Docker 在 2024 年慶祝開源 11 週年，Kubernetes 則迎來 10 週年。

## DevOps 工具鏈

| 領域 | 工具 | 2024 亮點 |
|------|------|-----------|
| CI/CD | GitHub Actions | AI 工作流程、Copilot 整合 |
| IaC | Terraform / Pulumi | 更多語言支援 |
| 監控 | OpenTelemetry | 業界標準確立 |
| 日誌管理 | Grafana Loki | 查詢效能提升 |

## 邊緣運算

2024 年被稱為「邊緣運算起飛年」。Cloudflare、Fastly、Vercel 等平台將邊緣函數推廣到主流應用中。

> 參考：https://www.google.com/search?q=cloud+DevOps+trends+2024
