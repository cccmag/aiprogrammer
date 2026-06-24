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
