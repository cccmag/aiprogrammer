# Chromium 專案與開放原始碼

## Chromium 專案介紹

### Chromium vs Chrome

許多人好奇 Chromium 和 Chrome 的關係：

| 專案 | 說明 |
|------|------|
| Chromium | 開放原始碼專案，完整功能 |
| Chrome | Google 發布的官方版本 |

```
Chromium（開放）         Chrome（Google 版本）
┌─────────────┐          ┌─────────────┐
│ 原始碼      │          │ 基於 Chromium│
│ MIT 授權    │    +     │ 封閉功能     │
│ 免費        │          │ Google 品牌 │
└─────────────┘          └─────────────┘
                              │
                              ├── 整合 Flash
                              ├── 自動更新
                              ├── 追蹤碼
                              └── 授權條款
```

### 為何要開源？

Google 選擇開源 Chromium 有多重考量：

```
開源策略的好處：

1. 開發者信任
   └── 任何人可審查程式碼，確保無隱藏追蹤

2. 社群貢獻
   └── 開發者能回報 Bug 和提交修補

3. 標準制定
   └── 推動網頁標準的開放發展

4. 生態系統
   └── 讓其他組織能基於 Chromium 開發瀏覽器
```

## Chromium 的架構

### 主要模組

```python
chromium_modules = {
    "WebKit": "HTML/CSS 解析和渲染引擎",
    "V8": "JavaScript 直譯器和 JIT 編譯器",
    "GPU Process": "圖形處理",
    "Plugin Process": "NPAPI 外掛程式",
    "Renderer Process": "分頁渲染程序",
    "Browser Process": "主程序，協調各模組"
}
```

### 分層架構

```
┌─────────────────────────────────────────┐
│            應用層 (Chrome UI)           │
├─────────────────────────────────────────┤
│                                         │
│  ┌───────────┐  ┌───────────┐           │
│  │  Renderer │  │  Renderer │  ...       │
│  │  Process  │  │  Process  │           │
│  └─────┬─────┘  └─────┬─────┘           │
│        │              │                 │
│  ┌─────┴──────────────┴─────┐          │
│  │     GPU Process            │          │
│  └──────────┬────────────────┘          │
│             │                            │
│  ┌──────────┴────────────────┐          │
│  │     Browser Process        │          │
│  └──────────┬────────────────┘          │
│             │                            │
│  ┌──────────┴────────────────┐          │
│  │     OS / Hardware          │          │
│  └─────────────────────────────┘          │
└─────────────────────────────────────────┘
```

## Chromium 的開放原始碼元件

### WebKit

WebKit 是 Chromium 使用的 HTML 渲染引擎：

```python
# WebKit 的組成部分

webkit_components = {
    "JavaScriptCore": "WebKit 的 JavaScript 引擎（Safari 使用）",
    "WebCore": "HTML/CSS 解析、DOM、渲染",
    "WebKit": "平台抽象層"
}

# 注意：Chrome 後來 fork WebKit 成為 Blink
```

### V8 JavaScript 引擎

V8 是 Google 開發的 JavaScript 引擎：

```python
v8_features = {
    "JIT 編譯": "直接編譯為機器碼",
    "隱式類型": "動態類型，最佳化推斷",
    "垃圾回收": "世代收集，漸進式回收",
    "內嵌快取": "加速重複函數呼叫"
}
```

## 授權條款

### 授權結構

Chromium 使用 BSD 授權：

```python
chromium_license = {
    "主要授權": "BSD License",
    "特點": [
        "可自由使用原始碼",
        "可修改後自行發布",
        "可商業使用",
        "需保留版權聲明"
    ],
    "專利授權": "包含專利授權"
}
```

### 第三方元件

Chromium 包含多個第三方元件：

| 元件 | 原始授權 |
|------|----------|
| WebKit | LGPL |
| V8 | BSD |
| Skia (2D 圖形) | BSD |
| SQLite | Public Domain |

## 社群參與

### 貢獻流程

```python
contribution_workflow = {
    "1. 回報 Bug": "在 Issue Tracker 描述問題",
    "2. 討論": "確認這是有效的 Bug 或功能需求",
    "3. 提交 Patch": "撰寫修改程式碼",
    "4. 程式碼審查": "由維護者審查",
    "5. 合併": "審查通過後合併到主線"
}
```

### 貢獻者角色

```python
contributors = {
    "Google 員工": "主要貢獻者，核心開發團隊",
    "其他公司": "如 Opera、Adobe、Samsung",
    "獨立開發者": "Bug 修復、功能增強",
    "社群": "測試、回報、文檔"
}
```

## 基於 Chromium 的瀏覽器

### 知名的 Chromium 分支

許多瀏覽器基於 Chromium 開發：

```python
chromium_forks = {
    "Google Chrome": "最著名的官方版本",
    "Opera": "2013 年後從 Presto 改用 Chromium",
    "Microsoft Edge": "2020 年後從 EdgeHTML 改用 Chromium",
    "Brave": "注重隱私的瀏覽器",
    "Vivaldi": "強調自訂性的瀏覽器",
    "Samsung Internet": "三星手機瀏覽器"
}
```

### 與上游保持同步

這些分支需要持續與 Chromium 同步：

```python
sync_challenges = {
    "頻率": "幾乎每天都會有新 commit",
    "衝突": "自行修改可能與上游衝突",
    "測試": "每次更新都需要完整測試",
    "資源": "需要專門團隊負責"
}
```

## 開發環境架設

### 取得原始碼

```bash
# 使用 depot_tools
git clone https://chromium.googlesource.com/chromium/tools/depot_tools.git
export PATH="$PATH:/path/to/depot_tools"

# 取得原始碼（這會下載數GB）
fetch --nohooks chromium

# 或只下載最新版本（較小）
fetch --nohooks chromium --filter=minimal

# 安裝依賴
./build/install-build-deps.sh

# 同步
gclient sync
```

### 編譯 Chromium

```bash
# 設定 GN
gn gen out/Release

# 編譯
ninja -C out/Release chrome
```

### 開發工作流程

```
開發流程：

1. 取出原始碼
2. 找到要修改的檔案
3. 撰寫修改
4. 編譯相關模組
5. 測試修改
6. 執行測試
7. 提交 Patch
```

## 測試框架

### Chromium 的測試類型

```python
test_types = {
    "單元測試": "測試獨立函數/類別",
    "整合測試": "測試多個元件互動",
    "效能測試": "Benchmark",
    " UI 測試": "自動化 UI 測試",
    "漸進式測試": "每次 commit 自動執行"
}
```

### 執行測試

```bash
# 執行特定測試
out/Release/bin/run_chromium_unittests

# 執行效能測試
out/Release/bin/run_chromium_perftests
```

## 參與社群

### 討論管道

```python
community_channels = {
    " Mailing Lists": "chromium-dev, blink-dev",
    " IRC": "#chromium, #blink-dev on Freenode",
    " Gerrit": "程式碼審查系統",
    "Issue Tracker": "Bug 追蹤"
}
```

### 文件資源

```python
documentation = {
    "官方 Wiki": "https://www.chromium.org/",
    "設計文件": "在 chromium.googlesource.com",
    "API 文件": "每個模組有單獨文件"
}
```

---

**延伸閱讀**

- [Chromium project official](https://www.google.com/search?q=Chromium+project+official)
- [Chromium+source+code](https://www.google.com/search?q=Chromium+source+code+download)
- [Chromium+development+guide](https://www.google.com/search?q=Chromium+development+guide)