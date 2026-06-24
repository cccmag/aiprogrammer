# 4. Google Cloud Platform 特色

## GCP 的起源與發展

Google 自 2000 年代初期就開始建設全球規模的資料中心，支撐 Search、Gmail、YouTube 等服務。2008 年以來，Google 逐步將這些內部使用的基礎設施對外開放，形成了今天的 Google Cloud Platform。2016 年的 GCP 已經從當初的 App Engine 單一服務，擴展為涵蓋運算、儲存、資料庫、大數據、機器學習的完整平台。

## 運算服務

**Compute Engine**：類似 AWS EC2 的 IaaS 服務。特色是提供自定義機器類型，可自由組合 CPU 與記憶體比例；以及承諾使用折扣（Committed Use Discounts），長期使用可享最高 57% 折扣。

**App Engine**：Google 原生的 PaaS 平台，早於 AWS Elastic Beanstalk 與 Azure App Service。支援 Python、Java、PHP、Go、Node.js。App Engine 會自動擴展，無需擔心容量規劃。

**Container Engine**：基於 Kubernetes 的容器管理服務，現在稱為 GKE（Google Kubernetes Engine）。Google 是 Kubernetes 的原始開發者，在容器編排領域有深厚底蘊。

## 大資料與分析

**BigQuery**：無伺服器的資料倉儲服務，可在秒級查詢 TB 等级的資料。採用預測性自動擴展，無需管理叢集大小。適合資料分析、商業智慧、日誌分析等場景。

**Cloud Dataflow**：統一的串流與批次資料處理服務，基於 Apache Beam SDK。可用於即時資料分析、ETL 工作流程、資料同步。

**Cloud Pub/Sub**：訊息佇列服務，設計用於高吞吐量、低延遲的即時訊息傳遞。支援即時與批次兩種消費模式。

**Dataproc**：托管的 Hadoop/Spark 服務，可快速建立和管理大數據叢集。按分鐘計費，不需要時可刪除叢集節省成本。

## 機器學習服務

**Cloud Machine Learning**：托管的機器學習平台，支援 TensorFlow 框架。可在 GPU 或 TPU（Google 自研的 AI 加速器）上訓練模型。

**Cloud Vision API**：預訓練的影像辨識 API，可識別物體、臉部、文字、情緒。无需訓練模型即可使用。

**Cloud Speech API**：語音轉文字 API，支援即時串流辨識與多種語言。

## 儲存服務

**Cloud Storage**：類似 AWS S3 的物件儲存服務，提供 Standard、Nearline、Coldline、Archive 四種儲存層級，按存取頻率定價。

**Cloud Bigtable**：NoSQL 列式資料庫，支援 PB 級別資料量，專為即時分析與時序資料設計。

**Cloud SQL**：托管的 MySQL 與 PostgreSQL，類似 AWS RDS。

## GCP 的獨特優勢

Google 在大資料處理與機器學習領域的積累是 GCP 最大的差異化優點。BigQuery 的查詢效能領先業界，Tensor Processing Unit（TPU）是專為深度學習設計的 AI 加速器，Kubernetes 的原生支援讓容器編排體驗最流暢。對於以資料分析或機器學習為核心的應用，GCP 是值得優先考慮的選擇。

## 參考資源

- https://www.google.com/search?q=Google+Cloud+Platform+GCP+服務+介紹+Compute+Engine+BigQuery+2016
- https://www.google.com/search?q=BigQuery+無伺服器+資料倉儲+SQL+查詢+大數據
- https://www.google.com/search?q=Kubernetes+Google+Container+Engine+GKE+容器編排+優勢