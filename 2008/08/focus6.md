# 負載均衡與高可用

## 負載均衡演算法

### 常見演算法

```python
load_balancing_algorithms = {
    'Round Robin': '依序分發到每個伺服器',
    'Weighted Round Robin': '根據權重分發',
    'Least Connections': '分發到連接數最少的',
    'IP Hash': '根據客戶端 IP 哈希分發',
    'URL Hash': '根據 URL 哈希分發'
}
```

### Python 簡單實現

```python
import hashlib

class LoadBalancer:
    def __init__(self, servers):
        self.servers = servers

    def get_server(self, key):
        if len(self.servers) == 0:
            return None
        hash_value = int(hashlib.md5(key.encode()).hexdigest(), 16)
        index = hash_value % len(self.servers)
        return self.servers[index]

# 使用
lb = LoadBalancer(['server1', 'server2', 'server3'])
server = lb.get_server('192.168.1.100')
```

## 健康檢查

### 類型

```python
health_check_types = {
    'TCP': '檢查 TCP 連接',
    'HTTP': '檢查 HTTP 回應',
    'HTTPS': '檢查 HTTPS 回應',
    'Custom': '自訂檢查腳本'
}
```

### 實現

```python
import socket

def check_health(host, port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(5)
        result = sock.connect_ex((host, port))
        sock.close()
        return result == 0
    except:
        return False
```

## 高可用架構

### 故障轉移

```python
# 故障轉移流程
failover_flow = [
    '健康檢查失敗',
    '從可用池移除故障節點',
    '流量切換到健康節點',
    '發送告警通知',
    '記錄故障日誌'
]
```

### 常見架構

```
          ┌─────────────┐
          │  Load       │
          │  Balancer   │
          └──────┬──────┘
                 │
    ┌────────────┼────────────┐
    │            │            │
┌───▼───┐   ┌───▼───┐   ┌───▼───┐
│Server1│   │Server2│   │Server3│
└───────┘   └───────┘   └───────┘
```

## 結論

負載均衡和高可用是確保服務穩定性的關鍵。

---

**延伸閱讀**

- [Load+balancing+algorithms](https://www.google.com/search?q=load+balancing+algorithms)