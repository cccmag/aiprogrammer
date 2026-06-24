# HTTP/2 與 gRPC：高效服務端

## 前言

HTTP/2 和 gRPC 是現代 API 架構的重要技術。

## HTTP/2 特性

```python
# 使用 hypercorn（ASGI 伺服器）
# 或使用 aiohttp

import aiohttp
import aiohttp.web

async def handler(request):
    return aiohttp.web.Response(text="Hello")

app = aiohttp.web.Application()
app.router.add_get('/', handler)
aiohttp.web.run_app(app, port=8000)
```

## gRPC

```protobuf
// proto/user.proto
syntax = "proto3";

service UserService {
    rpc GetUser (UserRequest) returns (UserResponse);
}

message UserRequest {
    string id = 1;
}

message UserResponse {
    string name = 1;
    string email = 2;
}
```

```python
import grpc
from concurrent import futures

class UserService(user_pb2_grpc.UserServiceServicer):
    def GetUser(self, request, context):
        return user_pb2.UserResponse(name="John", email="john@example.com")

server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
user_pb2_grpc.add_UserServiceServicer_to_server(UserService(), server)
server.add_insecure_port('[::]:50051')
server.start()
```

## 延伸閱讀

- [gRPC 官方文檔](https://www.google.com/search?q=grpc+python+tutorial)