# 實作簡化 REST API 框架：打造 MiniAPI

## 簡介

本期程式實作將帶領讀者從頭實作一個簡化的 REST API 框架 MiniAPI，幫助理解 API 伺服器的基本概念。

## 程式碼

```python
#!/usr/bin/env python3
"""
MiniAPI - A simplified REST API framework demo

這個程式演示了 REST API 框架的基本概念：
1. 路由系統
2. 請求處理
3. 簡單的 middleware
"""

from dataclasses import dataclass, field
from typing import Dict, List, Callable, Any, Optional
from enum import Enum
import json


class HTTPMethod(Enum):
    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    DELETE = "DELETE"
    PATCH = "PATCH"


@dataclass
class Request:
    method: HTTPMethod
    path: str
    body: Optional[Dict[str, Any]] = None
    headers: Dict[str, str] = field(default_factory=dict)
    query_params: Dict[str, str] = field(default_factory=dict)


@dataclass
class Response:
    status_code: int = 200
    body: Any = None
    headers: Dict[str, str] = field(default_factory=dict)


class Route:
    def __init__(self, pattern: str, method: HTTPMethod, handler: Callable):
        self.pattern = pattern
        self.method = method
        self.handler = handler


class MiniAPI:
    def __init__(self):
        self.routes: List[Route] = []
        self.middleware: List[Callable] = []

    def add_route(self, path: str, method: HTTPMethod,
                  handler: Callable):
        route = Route(path, method, handler)
        self.routes.append(route)

    def add_middleware(self, middleware: Callable):
        self.middleware.append(middleware)

    def get(self, path: str, handler: Callable):
        self.add_route(path, HTTPMethod.GET, handler)

    def post(self, path: str, handler: Callable):
        self.add_route(path, HTTPMethod.POST, handler)

    def put(self, path: str, handler: Callable):
        self.add_route(path, HTTPMethod.PUT, handler)

    def delete(self, path: str, handler: Callable):
        self.add_route(path, HTTPMethod.DELETE, handler)

    def match_route(self, path: str, method: HTTPMethod) -> Optional[Route]:
        for route in self.routes:
            if route.path == path and route.method == method:
                return route
        return None

    def handle_request(self, request: Request) -> Response:
        for mw in self.middleware:
            request = mw(request)

        route = self.match_route(request.path, request.method)
        if route:
            return route.handler(request)
        else:
            return Response(
                status_code=404,
                body={"error": "Not Found"}
            )

    def run(self, host: str = "localhost", port: int = 8080):
        print(f"MiniAPI server running on {host}:{port}")
        print("Try: curl http://localhost:8080/users")
        print("Or:  curl -X POST http://localhost:8080/users -d '{\"name\":\"張三\"}'")


def demo():
    print("\n" + "#" * 60)
    print("# MiniAPI - REST API Framework Demo")
    print("#" * 60 + "\n")

    app = MiniAPI()

    users_db = []

    def get_users(request: Request) -> Response:
        return Response(
            status_code=200,
            body={"users": users_db}
        )

    def create_user(request: Request) -> Response:
        if request.body and 'name' in request.body:
            user = {"id": len(users_db) + 1, "name": request.body['name']}
            users_db.append(user)
            return Response(status_code=201, body=user)
        return Response(status_code=400, body={"error": "Name required"})

    def get_user(request: Request) -> Response:
        user_id = int(request.path.split('/')[-1])
        user = next((u for u in users_db if u['id'] == user_id), None)
        if user:
            return Response(status_code=200, body=user)
        return Response(status_code=404, body={"error": "Not Found"})

    def delete_user(request: Request) -> Response:
        user_id = int(request.path.split('/')[-1])
        for i, u in enumerate(users_db):
            if u['id'] == user_id:
                users_db.pop(i)
                return Response(status_code=204, body=None)
        return Response(status_code=404, body={"error": "Not Found"})

    # 簡單的 middleware
    def logging_middleware(request: Request) -> Request:
        print(f"  -> {request.method.value} {request.path}")
        return request

    # 註冊路由
    app.add_middleware(logging_middleware)
    app.get("/users", get_users)
    app.post("/users", create_user)
    app.get("/users/:id", get_user)
    app.delete("/users/:id", delete_user)

    # 模擬請求
    print("Simulating requests:\n")

    # GET /users
    req = Request(HTTPMethod.GET, "/users")
    resp = app.handle_request(req)
    print(f"Response: {resp.status_code} - {resp.body}\n")

    # POST /users
    req = Request(HTTPMethod.POST, "/users",
                   body={"name": "張三"})
    resp = app.handle_request(req)
    print(f"Response: {resp.status_code} - {resp.body}\n")

    # GET /users/1
    req = Request(HTTPMethod.GET, "/users/1")
    resp = app.handle_request(req)
    print(f"Response: {resp.status_code} - {resp.body}\n")

    app.run()


if __name__ == "__main__":
    demo()
```

## 測試方式

```bash
python3 _code/api_demo.py
```

## 實作重點

1. **Route 類別**：儲存路徑模式和處理函數
2. **MiniAPI 類別**：管理路由和中間件
3. **Middleware**：請求處理的前置處理
4. **Request/Response**：封裝 HTTP 請求和回應

## 延伸學習

- 實作路徑參數解析（:id 語法）
- 實作錯誤處理
- 實作認證 middleware
- 實作更複雜的路由匹配

---

*本期程式實作到此結束。*