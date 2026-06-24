# 2. IaaS、PaaS、SaaS 服務模型

## 三種服務模型的定位

雲端服務依抽象層級由低到高分為 IaaS（基礎設施即服務）、PaaS（平台即服務）、SaaS（軟體即服務）。層級越低，控制權越大，但需要管理的面向越多；層級越高，使用越簡單，但客製化彈性越小。

## IaaS（基礎設施即服務）

IaaS 提供最基礎的虛擬化伺服器、儲存、網路資源。使用者自行管理作業系統、儲存、部署的應用程式，需要具備伺服器管理能力。常見的 IaaS 服務包括：

**虛擬伺服器**：AWS EC2、Azure Virtual Machines、Google Compute Engine。使用者可以自由選擇 CPU、記憶體、硬碟規格，隨時調整大小。

**區塊儲存**：AWS EBS、Azure Disk Storage、GCP Persistent Disk。提供高效且持久的區塊層級儲存，可當作虛擬機器的系統碟或資料碟。

**物件儲存**：AWS S3、Azure Blob Storage、GCP Cloud Storage。以 RESTful API 存取，適合儲存大量非結構化資料如圖片、影片、備份檔案。

**網路服務**：負載平衡器、防火牆、VPN、CDN。協助建立安全且高效的网络架构。

IaaS 的優點是彈性最大、可完全控制；缺點是需要自行管理作業系統更新、安全修補、應用程式部署。

## PaaS（平台即服務）

PaaS 在 IaaS 之上再封裝一層，自動處理作業系統、資料庫、Web 伺服器等底層工作。使用者只需上傳程式碼，平台負責執行環境的建置與擴展。

**應用程式執行環境**：AWS Elastic Beanstalk、Azure App Service、Google App Engine。支援多种程式語言與框架。

**資料庫服務**：AWS RDS、Azure SQL Database、Google Cloud SQL。由供應商自動處理備份、效能調校、版本升級。

**訊息佇列**：AWS SQS、Azure Service Bus、Google Cloud Pub/Sub。用於元件之間的非同步通訊。

**容器服務**：AWS ECS/EKS、Azure Container Service、Google Kubernetes Engine。簡化容器的部署與管理。

PaaS 的優點是大幅減少維運負擔、加快開發速度；缺點是受平台限制、某些底層功能無法自訂。

## SaaS（軟體即服務）

SaaS 是完整的應用程式服務，使用者直接使用軟體功能，無需安裝或維護。供應商負責所有底層基礎設施與應用程式的更新。

**企業應用**：Salesforce（CRM）、Microsoft Office 365（辦公軟體）、Slack（團隊溝通）。

**開發工具**：GitHub（程式碼托管）、Jenkins（持續整合）、New Relic（效能監控）。

**商業應用**：SAP、Oracle ERP、Google Workspace。

SaaS 的優點是立即可用、無需維護；缺點是功能受限於供應商、資料存放在第三方、訂閱費用長期可能高於授權買斷。

## 選擇建議

新創公司或小型團隊，建議從 PaaS 開始以降低維運成本；大型企業有特殊合規或客製需求，IaaS 提供更大的控制權；一般商務軟體需求則可考慮 SaaS 方案。

## 參考資源

- https://www.google.com/search?q=IaaS+PaaS+SaaS+差異+比較+雲端服務模型+2016
- https://www.google.com/search?q=AWS+EC2+S3+Elastic+Beanstalk+RDS+服務比較+介紹
- https://www.google.com/search?q=何時使用+IaaS+PaaS+SaaS+選擇+建議+抉擇