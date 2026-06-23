# AI 應用的持續交付（2020-2026）

## CI/CD for ML：從訓練到部署的管線

傳統軟體的 CI/CD 管線處理的是原始碼到可執行檔的轉換。ML 的 CI/CD 則需要處理一個更複雜的流程：資料 → 特徵 → 模型 → 評估 → 部署。

**持續整合（CI）**：每次程式碼變更時自動執行測試。在 ML 場景中，這包括資料驗證、特徵計算測試、模型訓練測試和評估測試。

**持續交付（CD）**：將通過測試的模型自動部署到生產環境。在 LLM 場景中，這還包括提示詞的部署。

```python
# ML CI/CD 管線示意
class MLPipeline:
    def __init__(self):
        self.stages = []
    
    def add_stage(self, name: str, fn):
        self.stages.append((name, fn))
    
    def run(self, context: dict) -> dict:
        for name, fn in self.stages:
            print(f"=== {name} ===")
            context = fn(context)
            if context.get("status") == "failed":
                print(f"管線在 {name} 階段失敗")
                break
        return context

# 定義管線階段
def validate_data(ctx):
    print(f"驗證資料集: {ctx['dataset']}")
    ctx["data_quality"] = 0.95
    return ctx

def train_model(ctx):
    print("開始訓練模型...")
    ctx["model_accuracy"] = 0.932
    ctx["model_path"] = "models/v3/model.pkl"
    return ctx

def evaluate_model(ctx):
    print(f"評估模型: accuracy={ctx['model_accuracy']}")
    if ctx["model_accuracy"] < 0.9:
        ctx["status"] = "failed"
    return ctx

def deploy_model(ctx):
    print(f"部署模型: {ctx['model_path']}")
    ctx["deployment_url"] = "https://api.example.com/v3/predict"
    return ctx

# 執行管線
pipeline = MLPipeline()
pipeline.add_stage("資料驗證", validate_data)
pipeline.add_stage("模型訓練", train_model)
pipeline.add_stage("模型評估", evaluate_model)
pipeline.add_stage("模型部署", deploy_model)

result = pipeline.run({"dataset": "sales_2026"})
```

## 模型 A/B 測試與漸進式發布

模型的發布不是一個二元操作（舊模型 → 新模型），而是一個漸進的過程：

```python
# 漸進式模型發布
class ProgressiveRollout:
    def __init__(self, model_a, model_b):
        self.model_a = model_a  # 當前穩定版本
        self.model_b = model_b  # 新版本
        self.traffic_split = 0.0  # B 的流量比例，從 0 開始
        self.metrics = {"a": [], "b": []}
    
    def set_traffic_split(self, percentage: float):
        self.traffic_split = percentage / 100.0
    
    def route_request(self, request) -> tuple:
        """根據流量分配路由請求"""
        import random
        if random.random() < self.traffic_split:
            response = self.model_b.predict(request)
            self.metrics["b"].append(response)
            return response, "b"
        response = self.model_a.predict(request)
        self.metrics["a"].append(response)
        return response, "a"
    
    def rollback(self):
        """完全回滾到模型 A"""
        self.traffic_split = 0.0
        print("已回滾到模型 A")
    
    def promote(self):
        """將模型 B 提升為穩定版本"""
        self.model_a = self.model_b
        self.traffic_split = 0.0
        print("模型 B 已提升為穩定版本")

# 發布策略
deploy = ProgressiveRollout(model_old, model_new)
deploy.set_traffic_split(1)    # 1% 流量到新模型
# ... 監控 24 小時 ...
deploy.set_traffic_split(5)    # 5%
# ... 監控 24 小時 ...
deploy.set_traffic_split(25)   # 25%
# ... 監控 ...
deploy.set_traffic_split(50)   # 50%
# ... 監控 ...
deploy.promote()               # 100%，新模型成為穩定版
```

## 提示詞的持續部署（CD for Prompts）

提示詞的變更頻率遠高於模型——你可能每天都要調整提示詞的措辭、格式或指令。因此，提示詞的持續部署需要更輕量級的流程：

```python
# 提示詞持續部署流程
class PromptCD:
    def __init__(self, registry: PromptRegistry):
        self.registry = registry
        self.deployment_history = []
    
    def deploy_canary(self, prompt: PromptTemplate, canary_percent=5):
        """金絲雀發布：只對小部分流量啟用新提示詞"""
        deployment = {
            "prompt": prompt,
            "strategy": "canary",
            "percent": canary_percent,
            "status": "deploying",
            "timestamp": datetime.now(),
        }
        self.deployment_history.append(deployment)
        return deployment
    
    def monitor_deployment(self, deployment_id: int, 
                          quality_gate: QualityGate) -> str:
        """監控發布狀態，決定下一步"""
        dep = self.deployment_history[deployment_id]
        metrics = self._collect_metrics(dep["prompt"].name)
        
        # 品質檢查
        result = quality_gate.evaluate(metrics)
        if result["status"] == "fail":
            self._rollback_prompt(dep["prompt"].name)
            return "rolled_back"
        
        # 逐步增加流量
        if dep["percent"] < 100:
            dep["percent"] = min(dep["percent"] * 2, 100)
            return f"increased_to_{dep['percent']}%"
        
        dep["status"] = "fully_deployed"
        return "fully_deployed"
    
    def _rollback_prompt(self, name: str):
        """自動回滾提示詞"""
        prev = self.registry.get_previous_version(name)
        print(f"提示詞 {name} 回滾至 {prev.version}")
```

## Infrastructure as Code for AI

AI 系統的基礎設施比傳統應用更複雜：GPU 驅動、CUDA 版本、模型服務框架、向量資料庫、快取層……手動管理這些是不可行的。Infrastructure as Code（IaC）是唯一可行的路徑。

```python
# 使用 Python 定義 AI 基礎設施（概念）
class AIInfrastructure:
    def __init__(self):
        self.services = {}
    
    def add_model_service(self, name: str, model: str, 
                          replicas: int, gpu_type: str):
        """定義模型服務"""
        self.services[name] = {
            "type": "model_service",
            "model": model,
            "replicas": replicas,
            "gpu": gpu_type,
            "autoscaling": {
                "min_replicas": replicas,
                "max_replicas": replicas * 4,
                "target_latency_ms": 500,
            },
        }
    
    def add_vector_store(self, name: str, dimension: int, 
                         index_type: str = "hnsw"):
        """定義向量資料庫"""
        self.services[name] = {
            "type": "vector_store",
            "dimension": dimension,
            "index_type": index_type,
            "replicas": 2,
        }
    
    def add_prompt_router(self, name: str):
        """定義提示詞路由器"""
        self.services[name] = {
            "type": "prompt_router",
            "strategy": "latency_based",
            "cache": {"enabled": True, "ttl_seconds": 3600},
        }
    
    def deploy(self):
        """生成部署配置（模擬）"""
        import json
        config = {
            "version": "1.0",
            "services": self.services,
            "monitoring": {
                "prometheus": True,
                "grafana": True,
                "alert_rules": {
                    "error_rate": "> 1% for 5m",
                    "p99_latency": "> 2s for 5m",
                },
            },
        }
        print(f"部署配置:\n{json.dumps(config, indent=2)}")
        return config

# 使用範例
infra = AIInfrastructure()
infra.add_model_service("llm-v2", "gpt-4o-mini", replicas=3, gpu_type="A100")
infra.add_vector_store("docs-index", dimension=1536)
infra.add_prompt_router("main-router")
infra.deploy()
```

## 完整的 MLOps 平台架構

將上述所有元件整合起來，形成一個完整的 MLOps/LLMOps 平台：

```python
# 整合式 MLOps 平台
class MLOpsPlatform:
    def __init__(self):
        self.registry = PromptRegistry()
        self.monitor = AIMonitor()
        self.tracer = AgentTracer()
        self.quality_gate = QualityGate({
            "accuracy": 0.85, "faithfulness": 0.8, "safety": 0.95
        })
        self.rollout = None
    
    def ci_pipeline(self, model_path: str, prompt: PromptTemplate):
        """整合 CI 管線"""
        # 1. 註冊提示詞
        self.registry.register(prompt)
        
        # 2. 評估模型
        accuracy = self._eval_model(model_path)
        
        # 3. 品質閘道
        result = self.quality_gate.evaluate({"accuracy": accuracy})
        
        if result["status"] == "pass":
            # 4. 漸進式發布
            self.rollout = ProgressiveRollout(model_old, model_new)
            return "deployed"
        return "rejected"
    
    def observability_dashboard(self):
        """可觀測性儀表板"""
        return {
            "model_health": self.monitor.get_health_report(),
            "prompt_versions": {
                name: [p.version for p in versions[-3:]]
                for name, versions in self.registry._store.items()
            },
            "recent_trajectories": [
                t.session_id for t in self.tracer.trajectories[-5:]
            ],
        }
```

從 MLOps 到 LLMOps 的演進，本質上是從「管理模型」到「管理 AI 系統」的轉變。這個轉變需要新的工具、新的思維，以及最重要的——新的組織文化。

---

**下一步**：[回到本期焦點](focus.md)

## 延伸閱讀

- [CI/CD for Machine Learning](https://www.google.com/search?q=CI+CD+for+machine+learning)
- [Prometheus + Grafana for ML Monitoring](https://www.google.com/search?q=Prometheus+Grafana+ML+monitoring)
- [Infrastructure as Code for AI](https://www.google.com/search?q=Infrastructure+as+Code+AI)
- [MLOps 平台設計](https://www.google.com/search?q=MLOps+platform+design+patterns)
