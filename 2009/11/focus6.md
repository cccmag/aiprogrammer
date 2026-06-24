# API 閘道設計：統一接口

## API 閘道的功能

### 為什麼需要 API 閘道？

```markdown
# API 閘道的價值

1. 統一入口
   - 單一 URL
   - 簡化客戶端

2. 安全控制
   - 認證
   - 授權
   - 速率限制

3. 監控和分析
   - 使用統計
   - 效能監控

4. 請求路由
   - 版本控制
   - A/B 測試
```

## 實作

```python
# 簡化的 API 閘道

class APIGateway:
    def __init__(self):
        self.routes = {}
        self.middleware = []

    def add_route(self, path, backend):
        self.routes[path] = backend

    def add_middleware(self, func):
        self.middleware.append(func)

    def handle_request(self, request):
        # 應用中介軟體
        for mw in self.middleware:
            request = mw(request)

        # 路由
        route = self.routes.get(request.path)
        if route:
            return route.forward(request)
        else:
            return 404, {"error": "Not Found"}
```

## 速率限制

```python
# 簡單的速率限制

from collections import defaultdict
import time


class RateLimiter:
    def __init__(self, max_requests, window):
        self.max_requests = max_requests
        self.window = window
        self.requests = defaultdict(list)

    def is_allowed(self, client_id):
        now = time.time()
        # 清除過期的請求記錄
        self.requests[client_id] = [
            t for t in self.requests[client_id]
            if now - t < self.window
        ]
        if len(self.requests[client_id]) >= self.max_requests:
            return False
        self.requests[client_id].append(now)
        return True
```

## 結語

API 閘道是現代 API 架構的核心元件，提供了統一入口和安全控制。

---

*本篇文章為「AI 程式人雜誌 2009 年 11 月號」焦點系列之一。*