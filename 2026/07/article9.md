# Antigravity：AI 驅動的意圖驅動開發平台

## 前言

當我們談論軟體開發的未來，大多數討論都圍繞著 AI 輔助程式碼生成——GitHub Copilot、Cursor、Codeium 等工具協助開發者逐行撰寫程式碼。然而，有一家名為 **Antigravity** 的新創公司正在翻轉這個劇本：與其讓 AI 輔助人類寫程式，不如讓人類直接告訴 AI「想要什麼」，由 AI 全權負責從規格到部署的完整流程。這個方法被稱為**意圖驅動開發（Intent-Driven Development, IDD）**。

本文將深入探討 Antigravity 平台的核心理念、工作流程、技術架構，並透過一個 Rust Web 服務的實際案例，展示這個平台如何重新定義軟體開發的邊界。

---

## 一、何謂意圖驅動開發？

意圖驅動開發的核心思想非常簡單：**開發者只需要表達「做什麼」（What），不需要關心「怎麼做」（How）**。

在傳統開發流程中，工程師花費大量時間在以下活動上：

- 將需求轉化為技術規格
- 選擇框架與函式庫
- 撰寫樣板程式碼（boilerplate）
- 設定 CI/CD 管線
- 編寫測試與文件
- 部署與監控基礎設施

Antigravity 認為，這些活動的本質是重複性的模式識別與實作，而現代的大型語言模型（LLM）已經有能力將這些工作自動化。真正的創造性工作在於**定義意圖**——也就是清楚描述你希望系統做什麼、有哪些限制條件、以及如何驗證成功。

### 1.1 意圖的結構

在 Antigravity 中，一份完整的「意圖規格」包含以下元素：

| 元素 | 說明 | 範例 |
|------|------|------|
| **目標描述** | 自然語言描述想要的系統 | 「一個使用者註冊與登入的 REST API」 |
| **功能需求** | 清單式的功能列表 | 「支援 Email + 密碼登入」、「支援 JWT Token」 |
| **非功能需求** | 效能、安全、可擴展性要求 | 「回應時間 < 200ms」、「支援 OAuth 2.0」 |
| **技術偏好** | 語言、框架、基礎設施選擇 | 「使用 Rust + Axum」、「部署到 AWS Lambda」 |
| **驗證條件** | 如何確認實作正確 | 「所有端點通過整合測試」、「壓力測試達 1000 RPS」 |

---

## 二、平台工作流程

Antigravity 的開發循環可以概括為五個階段：

### 2.1 定義意圖（Define Intent）

開發者使用 Markdown 或網頁編輯器撰寫意圖規格檔。這是一份純文字文件，沒有任何程式碼。例如：

```yaml
# intent.md
name: blog-api
description: A RESTful blog API with user authentication and post management
language: rust
framework: axum
database: postgresql
deployment: docker-compose

features:
  - user registration with email verification
  - JWT-based authentication
  - CRUD for blog posts
  - pagination and search
  - rate limiting

constraints:
  - responses must be under 200ms p99
  - all inputs must be validated
  - passwords hashed with argon2

tests:
  - unit tests for all handlers
  - integration tests for all endpoints
  - load test: 500 concurrent users
```

### 2.2 自動生成（Auto-Generate）

Antigravity 將意圖規格傳送至其專屬的 LLM 引擎，該引擎經過數十萬個開源專案與生產應用的微調訓練。生成結果包含：

- 完整的專案結構與 `Cargo.toml`
- 所有原始碼檔案（路由、模型、資料庫遷移、中介軟體）
- 測試程式碼（單元測試、整合測試、負載測試腳本）
- Dockerfile 與 docker-compose.yml
- CI/CD 配置（GitHub Actions 或 GitLab CI）
- API 文件（OpenAPI/Swagger 規格）

### 2.3 人工審查（Human Review）

開發者檢視生成的程式碼，可以：

- 逐行審查關鍵邏輯
- 提出修改要求（「改用 `thiserror` 處理錯誤」）
- 新增或移除功能（「加上 rate limiting 中介軟體」）
- 直接手動修改任何檔案

審查完成後，開發者按下「批准」按鈕。

### 2.4 自動測試與驗證（Auto-Test & Verify）

Antigravity 自動執行：

1. **編譯檢查**：確保程式碼通過編譯
2. **靜態分析**：執行 clippy、rustsec 審計
3. **單元測試**：執行所有 `cargo test`
4. **整合測試**：啟動測試容器執行端到端測試
5. **安全掃描**：檢查相依套件中的已知漏洞
6. **效能基準**：執行負載測試並比對意圖中的 SLA

任何失敗會回饋給 LLM 引擎進行自動修正，最多重試三次。

### 2.5 持續部署（Continuous Deploy）

驗證通過後，Antigravity 自動：

- 建立 Docker 映像檔
- 推送至容器註冊表
- 更新 Kubernetes 部署或更新 docker-compose 服務
- 設定 DNS 與 TLS
- 配置監控與日誌聚合

整個流程從意圖到生產環境，典型案例可在 **15 分鐘內**完成。

---

## 三、與傳統開發流程的對比

為了更具體地理解意圖驅動開發的影響，我們將一個典型 Web 服務的開發流程進行比較：

| 階段 | 傳統開發 | Antigravity IDD |
|------|----------|-----------------|
| 需求分析 | 1-3 天 | 1-2 小時 |
| 技術選型 | 半天 ~ 1 天 | 自動（依意圖偏好） |
| 架構設計 | 1-3 天 | 自動生成 |
| 程式碼撰寫 | 1-2 週 | 分鐘級 |
| 測試撰寫 | 2-5 天 | 自動生成 |
| CI/CD 設定 | 半天 ~ 1 天 | 自動生成 |
| 部署 | 1-2 天 | 自動部署 |
| **總計** | **1-4 週** | **數小時 ~ 1 天** |

當然，這樣的比較忽略了前期學習成本與後期維護的差異。Antigravity 並非萬能——當專案需要高度客製化的商業邏輯或複雜的領域知識時，人工編寫仍然是必要的。

---

## 四、實際案例：用 Antigravity 開發 Rust Web 服務

讓我們實際走一遍使用 Antigravity 開發一個 Rust 部落格 API 的過程。

### 4.1 撰寫意圖

開發者建立 `intent.yaml`：

```yaml
name: rust-blog-api
description: Blog API with user auth and post management
language: rust
framework: axum
database: postgresql
orm: sqlx
deployment: docker-compose

features:
  - register/login with JWT
  - create/update/delete posts
  - list posts with pagination
  - search posts by title
  - role-based access (admin, editor, reader)

auth:
  provider: jwt
  hashing: argon2
  session_expiry: 24h

tests:
  - unit: true
  - integration: true
  - coverage_threshold: 80
```

### 4.2 生成結果

Antigravity 在 45 秒後生成以下專案結構：

```
rust-blog-api/
├── Cargo.toml
├── Dockerfile
├── docker-compose.yml
├── .env.example
├── src/
│   ├── main.rs
│   ├── lib.rs
│   ├── config.rs
│   ├── routes/
│   │   ├── mod.rs
│   │   ├── auth.rs
│   │   └── posts.rs
│   ├── models/
│   │   ├── mod.rs
│   │   ├── user.rs
│   │   └── post.rs
│   ├── handlers/
│   │   ├── mod.rs
│   │   ├── auth_handler.rs
│   │   └── post_handler.rs
│   ├── middleware/
│   │   ├── mod.rs
│   │   └── auth.rs
│   ├── db/
│   │   ├── mod.rs
│   │   └── migrations/
│   └── error.rs
├── tests/
│   ├── common/
│   │   └── mod.rs
│   ├── auth_test.rs
│   └── post_test.rs
└── openapi.yaml
```

### 4.3 程式碼片段範例

生成的路由定義：

```rust
// src/routes/posts.rs
use axum::{
    extract::{Path, Query, State},
    routing::{get, post, put, delete},
    Router, Json,
};
use crate::handlers::post_handler;
use crate::models::post::PostFilter;
use crate::middleware::auth::RequireAuth;

pub fn post_routes() -> Router<AppState> {
    Router::new()
        .route("/api/posts", get(list_posts).post(create_post))
        .route("/api/posts/:id", get(get_post)
            .put(update_post)
            .delete(delete_post))
        .route("/api/posts/search", get(search_posts))
}

async fn list_posts(
    State(state): State<AppState>,
    Query(filter): Query<PostFilter>,
) -> Result<Json<PaginatedPosts>, AppError> {
    let posts = state.post_repo.list(&filter).await?;
    Ok(Json(posts))
}
```

生成的資料庫遷移：

```sql
-- db/migrations/001_create_users.sql
CREATE TABLE IF NOT EXISTS users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    role VARCHAR(20) NOT NULL DEFAULT 'reader',
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
```

### 4.4 審查與部署

開發者審查程式碼後，發現需要加上 rate limiting 中介軟體，於是在審查介面中輸入：「在路由層級加入 `governor` 的 rate limiting，每分鐘每 IP 最多 60 個請求。」

Antigravity 在 10 秒內生成修改，開發者批准後，系統自動執行測試套件（全部 37 個測試通過），建立 Docker 映像檔，並部署至本機的 docker-compose 環境。從意圖撰寫到服務上線，總共耗時 **23 分鐘**。

---

## 五、Antigravity 的技術架構

Antigravity 平台的後端架構由以下核心元件組成：

### 5.1 意圖解析引擎（Intent Parser）

將自然語言意圖規格轉換為結構化的中間表示（Intermediate Representation, IR）。使用自訂的 LLM 搭配結構化輸出（JSON mode），確保意圖中的每個元素都被正確解析。

### 5.2 程式碼生成器（Code Generator）

採用**多階段生成策略**：

1. **架構生成**：根據 IR 決定專案結構、框架選擇、資料庫 schema
2. **骨架生成**：產生所有檔案的框架，包括 module 宣告、trait 定義、錯誤型別
3. **邏輯生成**：逐個檔案填入實作邏輯，每個檔案以獨立 LLM 調用生成
4. **整合生成**：產生 glue code、中間件註冊、路由掛載
5. **基礎設施生成**：Dockerfile、CI/CD、文件

每個階段都有獨立的驗證閘道，確保前一階段的輸出品質。

### 5.3 驗證沙箱（Verification Sandbox）

每次生成後，Antigravity 啟動隔離的 Docker 容器：

```
驗證管線：
1. cargo check         → 編譯錯誤檢測
2. cargo clippy        → 程式碼風格與潛在問題
3. cargo test          → 單元與整合測試
4. cargo audit         → 安全性審計
5. cargo tarpaulin     → 測試覆蓋率
6. k6 load test        → 效能基準測試
```

驗證失敗時，錯誤訊息（包含編譯器輸出、測試失敗堆疊）回饋至 LLM 進行自動修正。

### 5.4 持續部署引擎（CD Engine）

支援多種部署目標：

- Docker Compose（本機開發）
- Kubernetes（生產環境）
- AWS Lambda / ECS
- Google Cloud Run
- Azure Container Apps

### 5.5 學習迴圈（Learning Loop）

Antigravity 記錄每次開發循環中的：

- 使用者的審查修改
- 驗證失敗的原因
- 部署後的生產指標

這些資料用來持續微調底層模型，使其生成品質隨著使用次數增加而提升。

---

## 六、意圖驅動開發的優缺點分析

### 6.1 優點

**開發速度大幅提升**：從需求到部署的時間從數週縮短至數小時，對於原型開發、MVP、內部工具等場景極具價值。

**降低進入門檻**：非專業開發者也能夠建立功能完整的應用程式。一個熟悉業務邏輯的產品經理，可以在 Antigravity 上獨立建立一個後端服務。

**減少樣板程式碼**：重複性的 CRUD、認證、資料庫操作等完全自動化，開發者專注於真正的商業邏輯。

**內建最佳實踐**：生成的程式碼遵循社群公認的最佳實踐（錯誤處理、安全性、測試覆蓋率），減少了新手開發者的常見錯誤。

**文件與測試自動化**：API 文件、單元測試、整合測試在生成時一併完成，解決了開發者最常拖延的兩項工作。

### 6.2 缺點與限制

**客製化深度不足**：當需要非標準的架構決策或複雜的領域邏輯時，生成的程式碼往往需要大量人工修改。Antigravity 擅長常見模式，但對於罕見需求的理解仍然有限。

**除錯難度增加**：當生成的程式碼出現錯誤時，開發者對程式碼的理解程度可能不如自己撰寫來得深入，導致除錯更加困難。這被稱為「生成程式碼的認知落差」。

**供應商鎖定風險**：意圖規格與平台深度綁定。如果未來 Antigravity 停止服務或改變定價策略，遷移成本可能很高。

**安全與合規疑慮**：將意圖（可能包含商業機密）傳送至雲端 LLM 引擎，對於受到嚴格法規約束的產業（金融、醫療、國防）可能構成風險。

**缺乏創造力與直覺**：軟體開發中經常需要基於經驗的直覺判斷——「這樣做雖然理論上不是最優，但團隊熟悉所以維修成本更低」。LLM 無法理解這種組織層面的權衡。

### 6.3 適用場景

| 適合 | 不適合 |
|------|--------|
| CRUD 應用程式 | 系統軟體（OS、資料庫引擎） |
| API 閘道與微服務 | 高效能即時系統 |
| 內部管理工具 | 嵌入式與 IoT 韌體 |
| MVP 與原型開發 | 遺留系統遷移（複雜商業邏輯） |
| 資料管道與 ETL | 安全關鍵系統 |

---

## 七、結論

Antigravity 代表的意圖驅動開發並不是要取代軟體工程師，而是要**重新定義工程師的角色**。當重複性的實作工作被自動化後，開發者的價值將從「如何撰寫程式碼」轉變為「如何定義問題」。這與過去十年 DevOps 將維運工作自動化、讓工程師專注於開發的趨勢如出一轍。

對於 Rust 生態系而言，Antigravity 的出現恰逢其時。Rust 以安全與效能著稱，但陡峭的學習曲線長期以來是採用瓶頸。意圖驅動開發讓團隊可以在享受 Rust 優勢的同時，繞過初期的學習障礙——至少對於常見的應用模式而言。

正如 Antigravity 創辦人 Sarah Chen 所說：「最好的程式碼，是那些不需要被寫出來的程式碼。」在這個 AI 時代，我們的工作不是與機器競爭寫程式，而是學會更精準地表達我們的意圖。

---

*本文撰寫時，Antigravity 平台仍處於公開測試階段。讀者可以至 [antigravity.dev](https://antigravity.dev) 申請試用。*

*本文為 AI 程式人雜誌 2026 年 7 月號「Rust 專題」系列文章之九。*
