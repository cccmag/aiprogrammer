# 部署策略與藍綠部署

## 前言

部署策略影響系統的可用性與風險。先進的部署方式可以大幅減少停機時間與回滾成本。

## 常見部署策略

| 策略 | 停機時間 | 風險 | 成本 |
|------|----------|------|------|
| 手工部署 | 長 | 高 | 低 |
| 滾動部署 | 零 | 中 | 中 |
| 藍綠部署 | 零 | 低 | 高 |
| 金絲雀部署 | 零 | 低 | 中 |

## 藍綠部署

```bash
#!/bin/bash
# blue-green-deploy.sh

APP_NAME="myapp"
NEW_VERSION=$1
BLUE_PORT=3000
GREEN_PORT=3001

echo "Starting blue-green deployment for version $NEW_VERSION"

# 啟動綠色環境（新版本）
echo "Starting green environment..."
docker run -d \
  --name ${APP_NAME}-green \
  -p $GREEN_PORT:3000 \
  ${APP_NAME}:${NEW_VERSION}

# 健康檢查
sleep 10
if curl -sf http://localhost:$GREEN_PORT/health > /dev/null; then
    echo "Green environment healthy"
    
    # 切換負載平衡
    echo "Switching load balancer..."
    iptables -t nat -I PREROUTING -p tcp --dport 80 -j REDIRECT --to-port $GREEN_PORT
    
    # 測試一段時間
    sleep 60
    
    # 停止藍色環境（旧版本）
    echo "Stopping blue environment..."
    docker stop ${APP_NAME}-blue
    docker rm ${APP_NAME}-blue
    
    # 重命名 green 為 blue（保持一致性）
    docker stop ${APP_NAME}-green
    docker rename ${APP_NAME}-green ${APP_NAME}-blue
    docker start ${APP_NAME}-blue
    
    iptables -t nat -R PREROUTING 1 -p tcp --dport 80 -j REDIRECT --to-port $BLUE_PORT
    
    echo "Deployment completed"
else
    echo "Health check failed, rolling back..."
    docker stop ${APP_NAME}-green
    docker rm ${APP_NAME}-green
    exit 1
fi
```

## 滾動部署

```yaml
# rolling-update.yml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: myapp-deployment
spec:
  replicas: 5
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 1
      maxUnavailable: 0
  template:
    spec:
      containers:
        - name: myapp
          image: myapp:2.0.0
```

## 金絲雀部署

```python
# canary_deployment.py
import random

class CanaryDeployment:
    def __init__(self, canary_percentage=10):
        self.canary_percentage = canary_percentage
    
    def route_request(self, user_id):
        # 根據 user_id 決定路由
        # 確保同一使用者每次都路由到相同版本
        hash_value = hash(user_id) % 100
        
        if hash_value < self.canary_percentage:
            return 'canary'  # 新版本
        return 'stable'  # 穩定版本
    
    def get_version(self, user_id):
        version = self.route_request(user_id)
        return {
            'canary': '2.0.0',
            'stable': '1.9.0'
        }[version]

# 使用
deployment = CanaryDeployment(canary_percentage=10)
user_version = deployment.get_version('user123')
print(f"Routing user123 to version {user_version}")
```

## 回滾策略

```python
# rollback_manager.py
from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional

@dataclass
class Deployment:
    version: str
    deployed_at: datetime
    status: str
    health_metrics: dict

class RollbackManager:
    def __init__(self):
        self.deployments: List[Deployment] = []
    
    def deploy(self, version: str) -> bool:
        print(f"Deploying version {version}...")
        deployment = Deployment(
            version=version,
            deployed_at=datetime.now(),
            status='deployed',
            health_metrics={}
        )
        self.deployments.append(deployment)
        
        # 監控健康狀況
        if self.check_health(version):
            print(f"Deployment {version} successful")
            return True
        else:
            print(f"Deployment {version} failed, rolling back...")
            self.rollback()
            return False
    
    def check_health(self, version: str) -> bool:
        # 模擬健康檢查
        return random.random() > 0.1  # 90% 成功率
    
    def rollback(self):
        if len(self.deployments) < 2:
            print("No previous version to rollback to")
            return False
        
        current = self.deployments.pop()
        current.status = 'rolled_back'
        
        previous = self.deployments[-1]
        print(f"Rolling back to version {previous.version}")
        
        # 執行回滾
        return True
```

## A/B 測試部署

```python
# ab_deployment.py
class ABTestDeployment:
    def __init__(self):
        self.variants = {
            'A': {'weight': 50, 'version': '1.0.0'},
            'B': {'weight': 50, 'version': '2.0.0'}
        }
    
    def get_variant(self, user_id: str) -> str:
        hash_value = hash(user_id) % 100
        cumulative = 0
        
        for variant, config in self.variants.items():
            cumulative += config['weight']
            if hash_value < cumulative:
                return variant
        
        return 'A'
    
    def get_version(self, variant: str) -> str:
        return self.variants[variant]['version']

# 使用
ab = ABTestDeployment()
variant = ab.get_variant('user123')
version = ab.get_version(variant)
print(f"User user123 sees variant {variant} (version {version})")
```

## 延伸閱讀

- [部署策略比較](https://www.google.com/search?q=deployment+strategies+comparison+2016)
- [藍綠部署實踐](https://www.google.com/search?q=blue+green+deployment+2016)
- [金絲雀部署](https://www.google.com/search?q=canary+deployment+2016)

---

*本篇文章為「AI 程式人雜誌 2016 年 11 月號」DevOps 系列之一。*