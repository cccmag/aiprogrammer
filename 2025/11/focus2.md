# 用戶端-伺服器架構

## 經典模型的再思考

用戶端-伺服器（Client-Server）架構是網路應用的基礎模型。從最早的 Web 1.0 到現代的雲原生應用，這個模型的基本結構始終不變，但實作方式持續演進。

---

## 兩層式架構

最簡單的形式：客戶端直接與伺服器通訊。

```
┌──────────┐     HTTP/WebSocket     ┌──────────┐
│  Client  │ ◄──────────────────────► │  Server  │
│ (瀏覽器)  │                        │ (單一節點) │
└──────────┘                        └──────────┘
```

### 優點

- **簡單**：架構直觀，除錯容易
- **部署方便**：一套後端服務搞定所有邏輯
- **適合原型開發**：快速驗證想法

### 缺點

- **單點故障**：伺服器掛掉，全部無法使用
- **擴展困難**：只能垂直擴展（升級硬體）
- **耦合度高**：前後端綁定，難以獨立迭代

---

## 三層式架構

加入 API 層和資料庫層，實現關注點分離。

```
┌──────────┐    ┌──────────────┐    ┌──────────┐
│  Client  │───►│  Application  │───►│ Database │
│ (前端)    │    │  (後端服務)    │    │ (資料庫)  │
└──────────┘    └──────────────┘    └──────────┘
```

### 三層各司其職

**表現層（Presentation Layer）**
- 處理用戶介面
- 輸入驗證
- 渲染資料

**應用層（Application Layer）**
- 業務邏輯
- 認證授權
- 工作流程編排

**資料層（Data Layer）**
- 資料儲存與檢索
- 資料完整性
- 備份與恢復

### 三層式的優勢

- **可維護性**：修改一層不影響其他層
- **可擴展性**：各層可以獨立擴展
- **安全性**：資料庫不對外暴露

---

## 無狀態設計原則

### 什麼是無狀態？

無狀態（Stateless）設計是指伺服器不儲存客戶端狀態，每個請求都包含處理所需的所有資訊。

```python
# 有狀態（Stateful）— 不適合大規模擴展
class SessionManager:
    def __init__(self):
        self.sessions = {}  # 儲存在記憶體中
    def get_user(self, session_id):
        return self.sessions.get(session_id)

# 無狀態（Stateless）— 適合橫向擴展
# 使用 JWT 或外部 Session Store
# @app.get("/api/user")
# def get_user(token: str):
#     user_id = decode_jwt(token)
#     return db.query(User).get(user_id)
```

### 為何無狀態重要？

在水平擴展場景中，有狀態設計會導致問題：

```
無狀態（正確）
  Client ──→ Load Balancer ──→ Server A（處理）
  Client ──→ Load Balancer ──→ Server B（處理）
  // 任何伺服器都能處理任何請求

有狀態（有問題）
  Client ──→ Load Balancer ──→ Server A（有 session）
  Client ──→ Load Balancer ──→ Server B（沒有 session！）
  // 需要黏性 Session（Sticky Session）或集中式 Session Store
```

### 實際作法

將狀態外移到外部儲存：
- Redis 儲存 Session 資料
- JWT（JSON Web Token）將狀態編碼在 Token 中
- 前端的 Local Storage

---

## 水平擴展 vs 垂直擴展

### 垂直擴展（Scale Up）

升級單一伺服器的硬體規格。

```
┌───────────────────────┐
│    原始伺服器            │
│   CPU: 4 cores        │
│   RAM: 16 GB          │
│   Disk: 500 GB        │
└───────────────────────┘
          │
          ▼
┌───────────────────────┐
│    升級後伺服器          │
│   CPU: 32 cores       │
│   RAM: 128 GB         │
│   Disk: 2 TB          │
└───────────────────────┘
```

**優點**：簡單、不改架構、維護容易
**缺點**：有硬體上限、成本急劇上升

### 水平擴展（Scale Out）

增加伺服器的數量。

```
         ┌──────────────┐
         │ Load Balancer│
         └──────┬───────┘
          ┌─────┼──────┐
          │     │      │
     ┌────┘ ┌───┘  ┌──┘
  ┌──▼──┐┌──▼──┐┌──▼──┐
  │Srv A││Srv B││Srv C│
  └─────┘└─────┘└─────┘
```

**優點**：理論上無限擴展、成本線性成長
**缺點**：架構複雜、需處理分散式問題

---

## 實際案例：電商平台架構演進

### 第一階段：單體兩層架構

```
前端 + 後端 + 資料庫 都在同一台伺服器上
適合：日活 1000 用戶以下
```

### 第二階段：三層分離

```
前端靜態檔案放在 CDN
後端 API 部署在應用伺服器叢集
資料庫使用主從複寫
適合：日活 10 萬用戶
```

### 第三階段：微服務化

```
前端拆為多個 SPA/Mobile App
後端拆分為用戶服務、商品服務、訂單服務
資料庫按領域拆分，引入訊息佇列
適合：日活 100 萬以上
```

---

## 總結

用戶端-伺服器架構是所有 Web 系統的基礎。理解兩層與三層的差異、掌握無狀態設計原則、區分水平與垂直擴展的適用場景，是設計大規模系統的必備知識。

---

## 延伸閱讀

- [Client-Server Architecture](https://www.google.com/search?q=client+server+architecture+patterns)
- [Stateless Design Principles](https://www.google.com/search?q=stateless+architecture+design+principles)
- [Horizontal vs Vertical Scaling](https://www.google.com/search?q=horizontal+vs+vertical+scaling+system+design)

---

*本篇文章為「AI 程式人雜誌 2026 年 11 月號」系統設計系列之二。*
