# 效能測試與壓力測試

## 前言

效能測試驗證系統在正常負載下的表現，壓力測試則找出系統的極限與脆弱點。兩者都是確保軟體品質的重要環節。

## 效能測試類型

| 類型 | 目標 | 指標 |
|------|------|------|
| 負載測試 | 正常預期負載 | 回應時間、吞吐量 |
| 壓力測試 | 超越正常負載 | 臨界點、錯誤率 |
| 耐久測試 | 長時間運行 | 記憶體洩漏、資源消耗 |
| 尖峰測試 | 瞬間高負載 | 恢復能力 |

## Python 效能測試：locust

```python
# locustfile.py
from locust import HttpUser, task, between

class WebsiteUser(HttpUser):
    wait_time = between(1, 5)
    
    @task
    def index_page(self):
        self.client.get("/")
    
    @task(3)
    def view_users(self):
        self.client.get("/api/users")
    
    @task(2)
    def create_user(self):
        self.client.post("/api/users", json={
            'email': 'test@example.com',
            'name': 'Load Test'
        })
    
    def on_start(self):
        self.client.post("/api/auth/login", json={
            'email': 'test@example.com',
            'password': 'password123'
        })
```

```bash
locust -f locustfile.py --host=http://localhost:3000
```

## Python 效能測試：pytest-benchmark

```python
# test_performance.py
import pytest

def fibonacci(n):
    if n < 2:
        return n
    return fibonacci(n-1) + fibonacci(n-2)

def fibonacci_iterative(n):
    if n < 2:
        return n
    a, b = 0, 1
    for _ in range(n-1):
        a, b = b, a + b
    return b

def test_fibonacci_benchmark(benchmark):
    result = benchmark(fibonacci, 20)
    assert result == 6765

def test_fibonacci_iterative_benchmark(benchmark):
    result = benchmark(fibonacci_iterative, 100)
    assert result == 354224848179261915075
```

```bash
pytest test_performance.py --benchmark-only
```

## HTTP 負載測試：wrk

```bash
# 安裝 wrk
brew install wrk

# 執行基準測試
wrk -t12 -c400 -d30s http://localhost:3000/api/users
```

輸出範例：
```
Running 30s test @ http://localhost:3000/api/users
  12 threads and 400 connections
  Thread Stats   Avg      Stdev     Max   +/- Stdev
    Latency     45.23ms    8.12ms  123.45ms   78.50%
    Req/Sec    892.34     124.56   1234.00    68.90%
  3545678 requests in 30.01s, 2.34GB read
Requests/sec: 118176.56
Transfer/sec:     79.87MB
```

## JMeter 基本設定

```xml
<!-- Basic Test Plan -->
<jmeterTestPlan version="1.2">
  <hashTree>
    <ThreadGroup>
      <stringProp name="ThreadGroup.num_threads">100</stringProp>
      <stringProp name="ThreadGroup.ramp_time">10</stringProp>
      <stringProp name="ThreadGroup.duration">300</stringProp>
      
      <hashTree>
        <HTTPSamplerProxy>
          <stringProp name="HTTP.method">GET</stringProp>
          <stringProp name="HTTP.url">/api/users</stringProp>
        </HTTPSamplerProxy>
      </hashTree>
    </ThreadGroup>
  </hashTree>
</jmeterTestPlan>
```

## 記憶體效能測試

```python
# memory_test.py
import pytest
import psutil
import os

def get_memory_usage():
    process = psutil.Process(os.getpid())
    return process.memory_info().rss / 1024 / 1024  # MB

def test_memory_efficiency():
    initial_memory = get_memory_usage()
    
    # 建立大量物件
    data = []
    for i in range(100000):
        data.append({'id': i, 'value': 'x' * 100})
    
    final_memory = get_memory_usage()
    increase = final_memory - initial_memory
    
    # 記憶體增長不應超過 200MB
    assert increase < 200, f"Memory increase too high: {increase:.2f}MB"
```

## 壓力測試腳本

```python
# stress_test.py
import threading
import time
import requests

class StressTester:
    def __init__(self, url, num_threads=10, duration=60):
        self.url = url
        self.num_threads = num_threads
        self.duration = duration
        self.results = []
        self.errors = []
    
    def make_request(self):
        try:
            start = time.time()
            response = requests.get(self.url)
            elapsed = time.time() - start
            self.results.append({
                'status': response.status_code,
                'time': elapsed
            })
        except Exception as e:
            self.errors.append(str(e))
    
    def run(self):
        threads = []
        end_time = time.time() + self.duration
        
        while time.time() < end_time:
            if len(threads) < self.num_threads:
                t = threading.Thread(target=self.make_request)
                t.start()
                threads.append(t)
            
            threads = [t for t in threads if t.is_alive()]
            time.sleep(0.01)
        
        for t in threads:
            t.join()
    
    def report(self):
        total = len(self.results) + len(self.errors)
        success_rate = len(self.results) / total * 100 if total > 0 else 0
        avg_time = sum(r['time'] for r in self.results) / len(self.results) if self.results else 0
        
        print(f"Total requests: {total}")
        print(f"Success rate: {success_rate:.2f}%")
        print(f"Average response time: {avg_time:.3f}s")
        print(f"Errors: {len(self.errors)}")
```

## 延伸閱讀

- [Locust 負載測試工具](https://www.google.com/search?q=locust+load+testing+tutorial+2016)
- [效能測試最佳實踐](https://www.google.com/search?q=performance+testing+best+practices+2016)
- [JMeter 教學](https://www.google.com/search?q=jmeter+tutorial+2016)

---

*本篇文章為「AI 程式人雜誌 2016 年 10 月號」軟體測試系列之一。*