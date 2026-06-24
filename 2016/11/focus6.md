# 自動化測試與部署（2013-2016）

## 前言

自動化測試與部署是 DevOps 的核心實踐。從提交到上線，每一步都應該自動化。

## 測試自動化層級

```
提交 → Lint → 單元測試 → 整合測試 → E2E測試 → 安全掃描 → 部署
 │        │         │          │          │          │          │
 Git     語法       快速       組件        完整        漏洞        自動化
 Hook   檢查       回饋       驗證        功能        檢測        到各環境
```

## 自動化測試設定

### npm Scripts

```json
{
  "scripts": {
    "test": "jest",
    "test:watch": "jest --watch",
    "test:ci": "jest --ci --coverage",
    "test:e2e": "cypress run",
    "lint": "eslint src/",
    "lint:fix": "eslint src/ --fix",
    "build": "webpack --mode production",
    "deploy": "npm run build && ./deploy.sh"
  }
}
```

### 整合 CI

```yaml
# .travis.yml
language: node_js
node_js:
  - "6"

cache:
  directories:
    - node_modules
    - ~/.npm

install:
  - npm install

script:
  - npm run lint
  - npm test
  - npm run build

after_success:
  - npm run coverage
```

## 自動化部署流程

### 部署狀態機

```python
# deploy_state.py
from enum import Enum

class DeployState(Enum):
    PENDING = "pending"
    BUILDING = "building"
    TESTING = "testing"
    DEPLOYING = "deploying"
    COMPLETED = "completed"
    FAILED = "failed"
    ROLLED_BACK = "rolled_back"

class Deployment:
    def __init__(self, version, environment):
        self.version = version
        self.environment = environment
        self.state = DeployState.PENDING
        self.logs = []
    
    def transition(self, new_state):
        self.logs.append(f"Transition: {self.state.value} -> {new_state.value}")
        self.state = new_state
    
    def can_deploy(self):
        return self.state == DeployState.COMPLETED
```

### 滾動部署

```python
# rolling_deploy.py
class RollingDeployment:
    def __init__(self, service, total_instances=5):
        self.service = service
        self.total_instances = total_instances
        self.updated = 0
    
    def deploy_new_version(self, new_version):
        while self.updated < self.total_instances:
            instance = self._get_next_instance()
            
            # 停止舊實例
            self._drain_instance(instance)
            self._update_instance(instance, new_version)
            self._health_check(instance)
            
            self.updated += 1
            self._wait_for_stabilization()
    
    def _get_next_instance(self):
        # 選擇最舊的實例更新
        pass
    
    def _wait_for_stabilization(self):
        import time
        time.sleep(10)  # 等待新實例穩定
```

## 藍綠部署

```bash
#!/bin/bash
# blue-green-deploy.sh

APP_NAME="myapp"
VERSION=$1
OLD_VERSION=$(docker ps | grep $APP_NAME | awk '{print $2}' | cut -d: -f2)

echo "Deploying version: $VERSION"
echo "Current version: $OLD_VERSION"

# 啟動新版本（綠）
docker run -d \
  --name ${APP_NAME}-green \
  --restart unless-stopped \
  -p 3001:3000 \
  ${APP_NAME}:${VERSION}

# 健康檢查
sleep 10
if curl -sf http://localhost:3001/health; then
    echo "Green deployment successful"
    
    # 切換流量
    iptables -I PREROUTING -p tcp --dport 3000 -m conntrack --ctstate NEW -j REDIRECT --to-ports 3001
    
    # 等待舊請求完成
    sleep 30
    
    # 停止舊版本（藍）
    docker stop ${APP_NAME}-blue 2>/dev/null || true
    docker rm ${APP_NAME}-blue 2>/dev/null || true
    
    # 重新標記
    docker stop ${APP_NAME}-green
    docker rename ${APP_NAME}-green ${APP_NAME}-blue
    docker start ${APP_NAME}-blue
    
    echo "Deployment completed"
else
    echo "Health check failed, rolling back..."
    docker stop ${APP_NAME}-green
    docker rm ${APP_NAME}-green
    exit 1
fi
```

## 部署驗證

```python
# deployment_validator.py
import requests
import time

class DeploymentValidator:
    def __init__(self, endpoint, timeout=60):
        self.endpoint = endpoint
        self.timeout = timeout
    
    def validate_health(self):
        start = time.time()
        while time.time() - start < self.timeout:
            try:
                resp = requests.get(f"{self.endpoint}/health", timeout=5)
                if resp.status_code == 200:
                    return True
            except:
                pass
            time.sleep(2)
        return False
    
    def validate_metrics(self):
        resp = requests.get(f"{self.endpoint}/metrics")
        data = resp.json()
        
        return {
            'cpu': data.get('cpu_usage', 0) < 80,
            'memory': data.get('memory_usage', 0) < 90,
            'requests': data.get('request_rate', 0) > 0
        }
    
    def run_smoke_tests(self):
        tests = [
            ("GET", "/api/users"),
            ("POST", "/api/users", {"name": "Test"}),
            ("GET", "/api/health"),
        ]
        
        for method, path, *args in tests:
            if method == "GET":
                resp = requests.get(f"{self.endpoint}{path}")
            elif method == "POST":
                resp = requests.post(f"{self.endpoint}{path}", json=args[0])
            
            if resp.status_code >= 500:
                return False
        return True
```

## 延伸閱讀

- [自動化部署策略](https://www.google.com/search?q=automated+deployment+strategies+2016)
- [滾動部署實踐](https://www.google.com/search?q=rolling+deployment+2016)
- [藍綠部署](https://www.google.com/search?q=blue+green+deployment+2016)

## 結語

自動化測試與部署大幅減少人為錯誤，加快交付速度。投資自動化，長期回報驚人。

---

*本篇文章為「AI 程式人雜誌 2016 年 11 月號」DevOps 系列之一。*