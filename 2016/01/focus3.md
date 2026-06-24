# 3. AWS 核心服務介紹

## AWS 發展現況

Amazon Web Services 自 2006 年推出以來，已經發展成為全球最大的雲端平台。截至 2016 年，AWS 提供超過 70 種服務，涵蓋運算、儲存、資料庫、網路、分析、機器學習等領域。財富 500 強企業中有許多是 AWS 的客戶。

## 運算服務

**EC2（Elastic Compute Cloud）**：最核心的雲端運算服務。提供多種執行個體類型，適合不同的工作負載。t2 系列適合開發測試環境，m4 系列是通用型，c4 系列專為運算優化，r4 系列則針對記憶體密集型應用。

**Lambda**：無伺服器運算服務，支援 Node.js、Python、Java、C# 等語言。依實際執行時間計費，適合事件驅動的微服務，例如影像處理、資料轉換、Web API 後端。

**Lightsail**：簡化版的 VPS 服務，適合不熟悉雲端的新手，提供預先設定好的伺服器環境。

## 儲存服務

**S3（Simple Storage Service）**：物件儲存服務，宣稱 11 個 9 的可用性（99.999999999%）。適合存放靜態網站資源備份、資料湖、各種非結構化資料。支援生命週期政策，可自動將舊資料遷移到較便宜的儲存層級。

**EBS（Elastic Block Store）**：區塊儲存服務，提供 IOPS（固態硬碟）與磁性硬碟兩種類型。只能掛載到單一 EC2 執行個體，適合需要高效讀寫的資料庫儲存。

**Glacier**：歸檔儲存服務，成本極低但取出資料需要數分鐘到數小時。適合法規遵循需要的長期資料保存。

## 資料庫服務

**RDS（Relational Database Service）**：支援 MySQL、PostgreSQL、Oracle、SQL Server、MariaDB。自動處理軟體更新、備份、效能調校，大幅簡化資料庫維運。

**DynamoDB**：NoSQL 資料庫服務，提供毫秒級延遲的效能表現，自動分片支援大規模擴展。

**ElastiCache**：記憶體快取服務，支援 Redis 與 Memcached。用於加速資料庫查詢或工作階段管理。

## 網路服務

**VPC（Virtual Private Cloud）**：讓使用者在 AWS 中建立隔離的虛擬網路環境。可控制 IP 範圍、子網路、路由表、閘道，模擬傳統資料中心的網路架構。

**Route 53**：DNS 服務，支援網域註冊、DNSSEC、智慧路由（根據地理位置、延遲自動選擇最佳伺服器）。

**CloudFront**：內容傳遞網路（CDN），在全球多個邊緣節點快取靜態內容，加速使用者存取。

## Lambda 的無伺服器革命

Lambda 重新定義了雲端運算的使用模式。傳統上，即使 Web 服務一個月只處理幾千次請求，也需要支付一台伺服器的費用。Lambda 只在使用者請求到達時才執行程式碼，按實際執行時間（100 毫秒為單位）計費，大幅降低了間歇性工作負載的成本。

## 參考資源

- https://www.google.com/search?q=AWS+EC2+S3+RDS+Lambda+核心服務+介紹+2016
- https://www.google.com/search?q=AWS+VPC+網路+虛擬私有雲+子網路+設定
- https://www.google.com/search?q=Lambda+無伺服器+運算+事件驅動+範例+應用場景