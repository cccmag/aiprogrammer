# 資料工程團隊結構

## 前言

資料工程是 AI 組織的骨幹。隨著資料規模和複雜度的增長，團隊結構直接影響交付效率和系統可靠性。本文探討三種常見的資料工程團隊組織模式。

## 集中式團隊

集中式團隊是初創公司的典型模式：一個中央資料團隊服務所有業務線。

```python
""" 模擬集中式團隊的工作流 """
from enum import Enum

class DataRequest:
    def __init__(self, team: str, priority: int, description: str):
        self.team = team
        self.priority = priority
        self.description = description

class CentralDataTeam:
    def __init__(self):
        self.backlog = []
        self.sla_hours = {1: 4, 2: 24, 3: 72}

    def submit_request(self, request: DataRequest):
        self.backlog.append(request)
        self.backlog.sort(key=lambda r: r.priority)
        print(f"[集中式團隊] 收到 {request.team} 的請求: {request.description}")
        print(f"  預計 {self.sla_hours[request.priority]} 小時內處理")

    def process_next(self):
        if self.backlog:
            req = self.backlog.pop(0)
            print(f"處理中: {req.description}")

central = CentralDataTeam()
central.submit_request(DataRequest("推薦系統", 1, "新增即時特徵管線"))
central.submit_request(DataRequest("風控", 2, "建立交易資料倉儲"))
```

## 嵌入式團隊

每個產品團隊有自己的資料工程師，與產品工程師緊密協作。

```python
class EmbeddedDataEngineer:
    def __init__(self, team_name: str):
        self.team_name = team_name
        self.pipelines = []

    def build_pipeline(self, name: str, source: str, destination: str):
        pipeline = {
            "name": name,
            "source": source,
            "destination": destination,
            "status": "running",
        }
        self.pipelines.append(pipeline)
        print(f"[嵌入式] {self.team_name} 團隊建立管線: {name}")

    def maintain(self):
        """即時回應產品團隊的資料需求"""
        print(f"[嵌入式] {self.team_name} 團隊正在維護 {len(self.pipelines)} 條管線")

class ProductTeam:
    def __init__(self, name: str):
        self.name = name
        self.data_engineer = EmbeddedDataEngineer(name)

recommendation = ProductTeam("推薦系統")
recommendation.data_engineer.build_pipeline(
    "user_embedding", "click_logs", "feature_store"
)
```

## 混合模式

大型組織通常採用混合模式：核心平台團隊 + 嵌入式資料工程師。

```python
class DataPlatformTeam:
    def __init__(self):
        self.platforms = {
            "資料湖": {"uptime": 99.9},
            "特徵儲存": {"uptime": 99.99},
            "排程器": {"uptime": 99.95},
        }

    def provide_service(self, platform_name: str):
        print(f"[平台團隊] 提供 {platform_name}，可用性 {self.platforms[platform_name]['uptime']}%")

    def add_feature(self, platform_name: str, feature: str):
        print(f"[平台團隊] 為 {platform_name} 新增功能: {feature}")

platform = DataPlatformTeam()
platform.provide_service("特徵儲存")
platform.add_feature("特徵儲存", "即時特徵服務")
```

## 結語

沒有一勞永逸的團隊結構。建議路徑：先集中式快速建立基礎設施，隨組織擴大轉向混合模式——平台團隊負責核心基建，嵌入式工程師深入業務。關鍵是保持清晰的責任邊界和高效的溝通機制。

---

**延伸閱讀**

- [資料工程團隊組織指南](https://www.google.com/search?q=data+engineering+team+structure+best+practices)
- [資料平台團隊設計](https://www.google.com/search?q=data+platform+team+architecture)
- [ML 團隊協作模式](https://www.google.com/search?q=ML+team+collaboration+model)
