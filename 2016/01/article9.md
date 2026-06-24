# CloudWatch 監控日誌

## CloudWatch 概述

Amazon CloudWatch 是 AWS 的監控服務，提供資源與應用程式的指標、日誌、警示功能。透過 CloudWatch，你可以了解系統的效能表現、及早發現異常、並在問題發生時自動采取行動。

## 主要功能

**指標（Metrics）**：AWS 服務會自動發布各項指標，如 CPU 使用率、網路流量、磁碟讀寫等。這些指標以 5 分鐘間隔收集（付費版可達 1 分鐘）。

**日誌（Logs）**：集中收集、儲存、分析應用程式日誌。CloudWatch Logs Agent 可安裝在 EC2 執行個體上自動收集日誌。

**警示（Alarms）**：當指標超過閾值時觸發警示，可自動發送通知或執行補救動作。

**事件（Events）**：即時事件處理，可根據事件模式自動觸發 Lambda 或其他動作。

## 查看與管理指標

```bash
# 列出可用的名稱空間
aws cloudwatch list-metrics --namespace AWS/EC2

# 取得 CPU 使用率
aws cloudwatch get-metric-statistics \
    --namespace AWS/EC2 \
    --metric-name CPUUtilization \
    --start-time 2016-01-01T00:00:00 \
    --end-time 2016-01-02T00:00:00 \
    --period 3600 \
    --statistics Average
```

## 建立警示

```bash
aws cloudwatch put-metric-alarm \
    --alarm-name high-cpu-alarm \
    --alarm-description "當平均 CPU 使用率超過 70% 時警示" \
    --namespace AWS/EC2 \
    --metric-name CPUUtilization \
    --threshold 70 \
    --comparison-operator GreaterThanThreshold \
    --statistic Average \
    --period 300 \
    --evaluation-periods 2 \
    --alarm-actions arn:aws:sns:us-east-1:123456789012:my-topic
```

## CloudWatch Logs 設定

在 EC2 執行個體上安裝 CloudWatch Logs Agent：

```bash
# 安裝
sudo yum install -y awslogs

# 設定（編輯 /etc/awslogs/awslogs.conf）
sudo vi /etc/awslogs/awslogs.conf

# 啟動服務
sudo service awslogs start
```

或在 Dockerfile 中直接安裝：

```dockerfile
RUN pip install awscli && \
    curl https://s3.amazonaws.com/aws-cloudwatch/downloads/latest/awslogs-agent-setup.py -O && \
    python3 awslogs-agent-setup.py --region us-east-1
```

## 儀表板

CloudWatch Dashboards 可將多個指標整合在同一畫面，方便一目了然地掌握系統狀態。可新增折線圖、數字顯示、警示狀態等多種 widget。

## 參考資源

- https://www.google.com/search?q=AWS+CloudWatch+監控+指標+日誌+警示+設定+教學+2016
- https://www.google.com/search?q=CloudWatch+Logs+Agent+EC2+安裝+設定+收集+日誌
- https://www.google.com/search?q=CloudWatch+Dashboards+警示+Alarm+notification+SES+SNS