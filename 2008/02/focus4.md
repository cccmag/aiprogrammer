# 多程序架構

## 為何需要多程序？

### 單一程序瀏覽器的問題

傳統瀏覽器使用單一程序，導致多種問題：

```python
single_process_problems = {
    "穩定性": "一個分頁當機導致全部當機",
    "安全性": "任何分頁的程式碼都能訪問系統",
    "效能": "所有分頁競爭同一資源",
    "回應性": "一個分頁的 JavaScript 會凍住全部"
}
```

### 分頁隔離的優點

```
多程序架構的優勢：

┌─────────┐   ┌─────────┐   ┌─────────┐
│ 分頁 1  │   │ 分頁 2  │   │ 分頁 3  │
│ 當機！  │   │ 正常    │   │ 正常    │
└────┬────┘   └────┬────┘   └────┬────┘
     │             │             │
     ▼             ▼             ▼
  不影響       不受影響      不受影響
  其他分頁     其他分頁      其他分頁
```

## Chromium 的程序模型

### 程序類型

```python
chromium_processes = {
    "Browser Process": "主程序，協調所有操作",
    "Renderer Process": "每個分頁一個，渲染網頁內容",
    "GPU Process": "處理圖形加速（可共享）",
    "Plugin Process": "每個外掛程式一個",
    "Utility Process": "處理網址列等工具"
}
```

### 預設程序分配

```python
default_process_allocation = {
    "每個分頁": "一個 Renderer Process",
    "每個網站": "一個 Renderer Process（同一網站的多個分頁共用）",
    "每個外掛": "一個 Plugin Process",
    "共享 GPU": "一個 GPU Process（可設定）"
}
```

### 程序隔離策略

```python
process_isolation = {
    "同一網站分頁": "共享同一 Renderer Process",
    "不同網站": "不同 Renderer Process",
    "好處": "防止 cross-site 攻擊"
}
```

## Renderer Process 的職責

### 分頁內部運作

```python
renderer_responsibilities = {
    "HTML 解析": "將 HTML 轉換為 DOM 樹",
    "CSS 解析": "套用樣式",
    "版面計算": "計算元素位置",
    "頁面繪製": "將內容繪製到記憶體",
    "JavaScript 執行": "執行頁面腳本",
    "DOM 操作": "響應使用者互動"
}
```

### 渲染程序的限制

renderer 程序在沙盒中執行，有諸多限制：

```python
sandbox_restrictions = {
    "檔案系統": "無法直接存取，需透過 Browser 程序",
    "網路": "需透過 Browser 程序代理",
    "顯示": "無法直接操作螢幕，需透過 GPU 程序",
    "系統資源": "受限的資源配額"
}
```

## 程序間通訊（IPC）

### IPC 機制

Chromium 使用自訂的 IPC 系統：

```python
# IPC 訊息流程

分頁 A ──→ 發送訊息 ──→ Browser 程序 ──→ 處理 ──→ 分頁 B

訊息類型：
├── 同步訊息：發送後等待回應
├── 非同步訊息：發送後立即返回
└── 雙向訊息：可多次來回
```

### IPC 訊息範例

```python
# 發送一個簡單的 IPC 訊息

# 在 Renderer 程序中
chrome.send('FetchIcon', {url: 'https://example.com/icon.ico'})

# 在 Browser 程序中處理
chrome.on('FetchIcon', function(request, sender) {
    // 處理請求，可能需要網路下載
    // 然後回傳結果
    return {iconData: iconBytes};
});
```

## 分頁與網站隔離

### 起源（Origin）概念

```
同一來源（Same Origin）：
┌─────────────────────────────────┐
│ https://example.com:443/       │
│  ──→ scheme: https            │
│  ──→ host: example.com        │
│  ──→ port: 443                │
└─────────────────────────────────┘
```

### 跨站分頁隔離

```python
cross_site_isolation = {
    "目的": "防止一個網站的攻擊影響其他網站",
    "實作": "不同網站使用不同 Renderer 程序",
    "同一網站": "多個分頁共享同一程序（節省資源）",
    "缺點": "一個網站的多個分頁同時當機"
}
```

## 記憶體管理

### 跨程序記憶體共享

```python
memory_sharing = {
    "共用視窗記憶體": "使用 SharedMemory",
    "指令碼記憶體": "每個程序獨立",
    "圖形資源": "透過 GPU Process 共享"
}
```

### 記憶體壓力處理

```python
memory_pressure_handling = {
    "程序優先級": {
        "前景分頁": "正常優先級",
        "背景分頁": "較低優先級",
        "休眠分頁": "可暫停 JavaScript"
    },
    "記憶體回收": "系統記憶體不足時，優先回收背景分頁"
}
```

## 穩定性

### 當機隔離

```python
crash_isolation = {
    "Renderer 當機": "只影響該分頁，顯示「噢！」錯誤頁",
    "Plugin 當機": "只影響該外掛，不影響其他內容",
    "GPU 當機": "可重啟 GPU 程序",
    "Browser 當機": "整個瀏覽器關閉"
}
```

### 錯誤恢復

```python
recovery_mechanisms = {
    "分頁當機": "使用者可重新整理該分頁",
    "Renderer 錯誤": "嘗試重啟程序",
    "頁面錯誤": "顯示錯誤訊息，不完全當機"
}
```

## 安全性

### 沙盒模型

```python
sandbox_model = {
    "目的": "限制惡意或錯誤程式碼的影響範圍",
    "實作": "作業系統層級的權限限制",
    "Renderer 限制": [
        "無法讀寫檔案",
        "無法直接網路連接",
        "無法與其他程序直接通訊"
    ]
}
```

### 安全分層

```
安全架構分層：

┌─────────────────────────────────────┐
│         使用者（信任）              │
├─────────────────────────────────────┤
│    Browser Process（高權限）         │
│    - 處理 UI                        │
│    - 管理 Cookie                     │
│    - 處理網址列                     │
├─────────────────────────────────────┤
│    Renderer Process（低權限、沙盒）   │
│    - 執行 JavaScript                 │
│    - 渲染頁面                        │
│    - 無系統存取權                    │
└─────────────────────────────────────┘
```

## 效能考量

### 資源開銷

多程序架構確實有額外開銷：

```python
multi_process_overhead = {
    "記憶體": "每個程序需要獨立記憶體空間",
    "啟動時間": "新建程序需要時間",
    "程序間通訊": "IPC 有延遲",
    "上下文切換": "作業系統程序切換開銷"
}
```

### 最佳化策略

```python
optimizations = {
    "程序共享": "同網站分頁共享程序",
    "程序回收": "一段時間後關閉空閒程序",
    "延遲啟動": "需要時才建立程序",
    "程序池": "預先建立程序池"
}
```

## 與其他瀏覽器的比較

### IE 的程序模型

```python
ie_process_model = {
    "IE7": "單一程序，所有分頁和工具列",
    "IE8": "可選的保護模式，增加安全性",
    "IE9": "更強的保護模式"
}
```

### Firefox 的程序模型

```python
firefox_process_model = {
    "早期": "單一程序（與 Chrome 相同問題）",
    "Electrolysis (2016)": "引入了多程序支援",
    "當前": "可設定的程序數量"
}
```

## 未來演進

### 程序模型的改進

```python
future_improvements = {
    "更細粒度": "每個 iframe 可能有自己的程序",
    "服務化": "將功能拆分為獨立的 Service",
    "省電": "最佳化背景程序的資源使用",
    "安全": "更強的隔離和許可權控制"
}
```

### 網頁工作者（Web Workers）

```python
web_workers_note = {
    "說明": "JavaScript 的執行緒，可分擔主執行緒工作",
    "隔離": "每個 Worker 在獨立執行緒/程序",
    "限制": "無法直接訪問 DOM"
}
```

---

**延伸閱讀**

- [Chromium+multi-process+architecture](https://www.google.com/search?q=Chromium+multi-process+architecture)
- [Process+per+tab+Chrome](https://www.google.com/search?q=Process+per+tab+Chrome)
- [Browser+sandbox+security](https://www.google.com/search?q=Browser+sandbox+security)