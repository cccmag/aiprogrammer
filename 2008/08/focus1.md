# 效能度量與監控

## 時間度量

### Critical Rendering Path

```python
# 頁面載入時間分解
page_load_time = {
    'DNS lookup': '20-100ms',
    'TCP connection': '30-100ms',
    'SSL handshake': '50-150ms',
    'Time to First Byte': '100-300ms',
    'Content download': '根據大小',
    'DOM parsing': '50-150ms',
    'Render': '50-100ms'
}
```

### Navigation Timing API

```javascript
// 使用 Navigation Timing API
var timing = performance.timing;
var pageLoadTime = timing.loadEventEnd - timing.navigationStart;
var networkLatency = timing.responseEnd - timing.requestStart;
```

## 效能工具

### Web 測速

```python
# 模擬網站速度測試
def measure_page_speed(url):
    import time
    import requests

    start = time.time()
    response = requests.get(url)
    end = time.time()

    return {
        'url': url,
        'time': end - start,
        'size': len(response.content),
        'speed': len(response.content) / (end - start) / 1024  # KB/s
    }
```

### 基準測試

```python
# 基準測試範例
def benchmark(func, iterations=100):
    import time
    times = []
    for _ in range(iterations):
        start = time.time()
        func()
        times.append(time.time() - start)
    return {
        'avg': sum(times) / len(times),
        'min': min(times),
        'max': max(times)
    }
```

## 監控系統

### 類型

```python
# 效能監控類型
monitoring = {
    'real_user_monitoring': 'RUM，收集真實使用者資料',
    'synthetic_monitoring': '主動探測，基準測試',
    'alerts': '異常告警'
}
```

## 結論

正確的度量是優化的第一步。建立持續的監控可以及早發現效能問題。

---

**延伸閱讀**

- [YSlow 與效能法則](focus7.md)
- [Navigation+Timing+API](https://www.google.com/search?q=Navigation+Timing+API)