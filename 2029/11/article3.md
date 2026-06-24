# Agent 身分與 DID

## 前言

在 Agent 經濟中，每個 Agent 需要一個獨一無二且可驗證的身分。傳統的帳號密碼系統無法滿足去中心化環境的需求。去中心化身分（DID）為 Agent 提供了自主可控的數位身分。

## DID 基礎

DID 的核心是「擁有者控制身分，而非第三方機構」。每個 DID 文件包含公鑰、服務端點與驗證方法。

```python
import json, hashlib
from dataclasses import dataclass, field
from typing import Optional

@dataclass
class DIDDocument:
    id: str
    public_key: str
    authentication: list[str]
    service: list[dict] = field(default_factory=list)
    created: str = ""

def generate_did(public_key: str) -> str:
    prefix = "did:agent:"
    suffix = hashlib.sha256(public_key.encode()).hexdigest()[:16]
    return prefix + suffix

def verify_did(did_doc: DIDDocument, message: str, signature: str) -> bool:
    from hashlib import sha256
    expected = sha256(message.encode()).hexdigest()
    return signature == expected
```

## Agent 身分註冊

Agent 在市場中註冊時需要提交 DID 文件並證明對私鑰的控制權：

```python
class AgentIdentityRegistry:
    def __init__(self):
        self.registry: dict[str, DIDDocument] = {}
    def register(self, did: str, doc: DIDDocument):
        self.registry[did] = doc
    def resolve(self, did: str) -> Optional[DIDDocument]:
        return self.registry.get(did)
    def verify_ownership(self, did: str, challenge: str, response: str) -> bool:
        doc = self.resolve(did)
        if not doc:
            return False
        expected = hashlib.sha256((challenge + doc.public_key).encode()).hexdigest()
        return response == expected
```

## 參考資料

- https://www.google.com/search?q=decentralized+identifier+DID+agent+identity
- https://www.google.com/search?q=W3C+DID+standard+agent+economy
- https://www.google.com/search?q=self+sovereign+identity+AI+agent
