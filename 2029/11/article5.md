# 智慧合約 for AI

## 前言

智慧合約讓 Agent 之間的交易自動化、透明化且不可竄改。在 AI 經濟中，智慧合約不僅處理金流，還可以管理資料使用權限、模型授權與運算資源分配。

## 合約設計

AI 服務的智慧合約需要處理獨特的條件：推論次數限制、資料隱私保護、模型權重浮水印等。

```python
import hashlib, time
from dataclasses import dataclass, field
from enum import Enum

class ContractState(Enum):
    PENDING = 1
    ACTIVE = 2
    COMPLETED = 3
    DISPUTED = 4

@dataclass
class AIServiceContract:
    contract_id: str
    provider: str
    consumer: str
    service_type: str
    price: float
    max_inferences: int
    inferences_used: int = 0
    state: ContractState = ContractState.PENDING
    deposit: float = 0.0
    created_at: float = field(default_factory=time.time)
```

## 合約執行引擎

模擬智慧合約的自動執行邏輯：

```python
class SmartContractEngine:
    def __init__(self):
        self.contracts: dict[str, AIServiceContract] = {}
    def deploy(self, contract: AIServiceContract):
        contract.state = ContractState.ACTIVE
        contract.deposit = contract.price * 0.2
        self.contracts[contract.contract_id] = contract
    def use_service(self, contract_id: str) -> bool:
        c = self.contracts.get(contract_id)
        if not c or c.state != ContractState.ACTIVE:
            return False
        if c.inferences_used >= c.max_inferences:
            c.state = ContractState.COMPLETED
            return False
        c.inferences_used += 1
        return True
    def finalize(self, contract_id: str):
        c = self.contracts.get(contract_id)
        if not c:
            return
        used_ratio = c.inferences_used / c.max_inferences
        c.state = ContractState.COMPLETED
```

## 參考資料

- https://www.google.com/search?q=smart+contract+AI+service+payment
- https://www.google.com/search?q=blockchain+autonomous+agent+contract
- https://www.google.com/search?q=decentralized+AI+model+licensing+smart+contract
