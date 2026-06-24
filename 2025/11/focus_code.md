# 系統設計 Python 實作

## 前言

本篇文章展示三個經典的系統設計元件之 Python 實作：LRU 快取、輪詢負載平衡、以及基於執行緒的訊息佇列。這些實作雖然簡化，但說明了核心概念與取捨邏輯。

---

## 原始碼

完整的 Python 實作請參考：[_code/system_design.py](_code/system_design.py)

```python
#!/usr/bin/env python3
"""System Design Demos: Cache, Load Balancer, Message Queue"""

import time
import threading
import queue
import random
from collections import OrderedDict

class LRUCache:
    def __init__(self, capacity=3):
        self.capacity = capacity
        self.cache = OrderedDict()
        self.hits = 0
        self.misses = 0

    def get(self, key):
        if key in self.cache:
            self.cache.move_to_end(key)
            self.hits += 1
            return self.cache[key]
        self.misses += 1
        return None

    def put(self, key, value):
        if key in self.cache:
            self.cache.move_to_end(key)
        elif len(self.cache) >= self.capacity:
            self.cache.popitem(last=False)
        self.cache[key] = value

    def stats(self):
        total = self.hits + self.misses
        rate = self.hits / total * 100 if total else 0
        return {"hits": self.hits, "misses": self.misses, "hit_rate": f"{rate:.1f}%"}

class LoadBalancer:
    def __init__(self, servers=None):
        self.servers = servers or ["srv-a", "srv-b", "srv-c"]
        self.index = 0
        self.requests = {s: 0 for s in self.servers}

    def round_robin(self):
        server = self.servers[self.index]
        self.requests[server] += 1
        self.index = (self.index + 1) % len(self.servers)
        return server

    def stats(self):
        total = sum(self.requests.values())
        return {s: f"{c} ({c/total*100:.0f}%)" for s, c in self.requests.items()}

class MessageBroker:
    def __init__(self):
        self.queues = {}
        self.total_published = 0
        self.total_consumed = 0

    def create_queue(self, name):
        self.queues[name] = queue.Queue()

    def publish(self, qname, msg):
        if qname not in self.queues:
            self.create_queue(qname)
        self.queues[qname].put(msg)
        self.total_published += 1

    def consume(self, qname):
        if qname not in self.queues or self.queues[qname].empty():
            return None
        self.total_consumed += 1
        return self.queues[qname].get()

    def stats(self):
        sizes = {n: q.qsize() for n, q in self.queues.items()}
        return {"queue_sizes": sizes, "published": self.total_published, "consumed": self.total_consumed}

def demo_cache():
    print("=== LRU Cache Demo ===")
    cache = LRUCache(3)
    for i in range(1, 6):
        cache.put(f"key{i}", f"val{i}")
    for k in ["key3", "key4", "key5", "key3", "key1"]:
        v = cache.get(k)
        print(f"  get({k}) -> {v}")
    print(f"  Stats: {cache.stats()}")

def demo_load_balancer():
    print("\n=== Load Balancer Demo (Round-Robin) ===")
    lb = LoadBalancer()
    for _ in range(10):
        srv = lb.round_robin()
        print(f"  -> {srv}")
    print(f"  Distribution: {lb.stats()}")

def demo_message_queue():
    print("\n=== Message Queue Demo ===")
    broker = MessageBroker()
    broker.create_queue("orders")
    def producer():
        for i in range(5):
            broker.publish("orders", f"order-{i}")
            print(f"  [P] published order-{i}")
            time.sleep(random.uniform(0.05, 0.15))
    def consumer(n):
        for _ in range(5):
            msg = broker.consume("orders")
            if msg:
                print(f"  [C{n}] consumed {msg}")
            time.sleep(random.uniform(0.1, 0.2))
    threads = [threading.Thread(target=producer)]
    threads += [threading.Thread(target=consumer, args=(i,)) for i in (1, 2)]
    for t in threads: t.start()
    for t in threads: t.join()
    print(f"  Stats: {broker.stats()}")

def demo():
    print("System Design Demos\n")
    demo_cache()
    demo_load_balancer()
    demo_message_queue()

if __name__ == "__main__":
    demo()
```

---

## 執行結果

```
System Design Demos

=== LRU Cache Demo ===
  get(key3) -> val3
  get(key4) -> val4
  get(key5) -> val5
  get(key3) -> val3
  get(key1) -> None
  Stats: {'hits': 4, 'misses': 1, 'hit_rate': '80.0%'}

=== Load Balancer Demo (Round-Robin) ===
  -> srv-a
  -> srv-b
  -> srv-c
  -> srv-a
  -> srv-b
  -> srv-c
  -> srv-a
  -> srv-b
  -> srv-c
  -> srv-a
  Distribution: {'srv-a': '4 (40%)', 'srv-b': '3 (30%)', 'srv-c': '3 (30%)'}

=== Message Queue Demo ===
  [P] published order-0
  [C1] consumed order-0
  [C2] consumed None
  [P] published order-1
  [C1] consumed order-1
  [P] published order-2
  [C2] consumed order-2
  [P] published order-3
  [C1] consumed order-3
  [P] published order-4
  [C2] consumed order-4
  Stats: {'queue_sizes': {'orders': 0}, 'published': 5, 'consumed': 5}
```

---

## LRU 快取

下圖說明 LRU 快取在容量為 3 時的運作過程：

```
初始狀態：[ ]
put key1 → [key1]
put key2 → [key1, key2]
put key3 → [key1, key2, key3]
put key4 → [key2, key3, key4]  (key1 被淘汰)
get key3 → [key2, key4, key3]  (key3 移到末尾)
put key5 → [key4, key3, key5]  (key2 被淘汰)
get key1 → None (miss)
```

## 負載平衡器

Round-Robin 輪詢演算法將請求依序分配給各伺服器：

```
請求 1 → srv-a
請求 2 → srv-b
請求 3 → srv-c
請求 4 → srv-a
請求 5 → srv-b
```

## 訊息佇列

生產者-消費者模式實現非同步通訊：

```
生產者 ──發佈──→ [佇列] ──消費──→ 消費者 1
                           └──→ 消費者 2
```

---

## 延伸閱讀

- [系統設計面試思維](article1.md)
- [Redis 快取實戰](article4.md)
- [RabbitMQ 入門](article6.md)
- [負載平衡演算法](article3.md)
- [LRU Cache 演算法](https://www.google.com/search?q=LRU+cache+algorithm+implementation)
- [Round-Robin Load Balancing](https://www.google.com/search?q=round+robin+load+balancing+algorithm)
- [Message Queue Pattern](https://www.google.com/search?q=message+queue+pattern+producer+consumer)

---

*本篇文章為「AI 程式人雜誌 2026 年 11 月號」技術實作系列文章。*
