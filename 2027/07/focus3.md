# 提示詞管理與版本控制（2022-2026）

## 提示詞即程式碼（Prompt as Code）

早期使用 LLM 時，提示詞只是手邊的文字檔——某個 Markdown 文件裡的一段話，或是 Slack 對話中的一行訊息。這在原型開發階段勉強可行，但當產品上線後，問題就來了：

- 「這個提示詞是誰改的？」
- 「上週的回覆品質比較好，發生了什麼事？」
- 「這個提示詞在 ChatGPT 上測試正常，但在 API 上為什麼不一樣？」

這些問題的答案都指向同一個方向：**提示詞應該像程式碼一樣管理**。

Prompt as Code 的核心思想是：提示詞是產品邏輯的一部分，它應該經歷與程式碼相同的開發生命週期——撰寫、版本控制、審查、測試、部署。

```python
# 提示詞即程式碼的標準結構
from dataclasses import dataclass
from datetime import datetime

@dataclass
class PromptTemplate:
    name: str
    version: str
    template: str
    params: list[str]
    author: str
    created_at: datetime
    description: str
    
    def render(self, **kwargs) -> str:
        return self.template.format(**kwargs)
    
    def validate(self) -> bool:
        """驗證提示詞模板是否合法"""
        required = self.extract_params()
        return all(p in required for p in self.params)
    
    def extract_params(self) -> set[str]:
        import re
        return set(re.findall(r'\{(\w+)\}', self.template))

# 使用範例
prompt = PromptTemplate(
    name="summarize",
    version="2.1.0",
    template="請用三句話總結以下文章：\n\n{article}\n\n重點：",
    params=["article"],
    author="alice",
    created_at=datetime.now(),
    description="文章摘要提示詞 v2",
)
```

## 提示詞版本管理策略

提示詞的版本管理與程式碼類似，但有幾個獨特的需求：

**Git + Registry 雙層架構**：Git 管理提示詞的程式碼變更歷史（什麼人、什麼時候、為什麼改了什麼），Registry 管理提示詞的運行時版本（目前線上跑的是哪個版本、可以回滾到哪個版本）。

**語義化版本（Semantic Versioning）**：提示詞也應該遵守語義化版本規範——主版號（不相容的變更）、次版號（向後相容的新功能）、修訂號（小修正）。

```python
# 提示詞 Registry
class PromptRegistry:
    def __init__(self):
        self._store: dict[str, list[PromptTemplate]] = {}
    
    def register(self, prompt: PromptTemplate):
        if prompt.name not in self._store:
            self._store[prompt.name] = []
        self._store[prompt.name].append(prompt)
        print(f"Registered {prompt.name} v{prompt.version}")
    
    def get_latest(self, name: str) -> PromptTemplate:
        return self._store[name][-1] if self._store.get(name) else None
    
    def get_version(self, name: str, version: str) -> PromptTemplate:
        for p in self._store.get(name, []):
            if p.version == version:
                return p
        return None
    
    def rollback(self, name: str, target_version: str) -> PromptTemplate:
        idx = None
        for i, p in enumerate(self._store.get(name, [])):
            if p.version == target_version:
                idx = i
                break
        if idx is not None:
            return self._store[name][idx]
        raise ValueError(f"Version {target_version} not found")
    
    def diff(self, name: str, v1: str, v2: str) -> list[str]:
        p1 = self.get_version(name, v1)
        p2 = self.get_version(name, v2)
        if not p1 or not p2:
            return []
        lines1 = p1.template.splitlines()
        lines2 = p2.template.splitlines()
        changes = []
        for i, (a, b) in enumerate(zip(lines1, lines2)):
            if a != b:
                changes.append(f"L{i+1}: - {a}")
                changes.append(f"L{i+1}: + {b}")
        return changes
```

## A/B 測試與漸進式發布

提示詞的變更不能直接上線——你永遠不知道一個小改動會對輸出品質造成什麼影響。A/B 測試是提示詞發布的標準流程。

```python
# 提示詞 A/B 測試框架
import random
import statistics

class PromptABTest:
    def __init__(self, control: PromptTemplate, variant: PromptTemplate, 
                 control_weight=0.5):
        self.control = control
        self.variant = variant
        self.control_weight = control_weight
        self.results: dict[str, list[float]] = {
            control.version: [],
            variant.version: [],
        }
    
    def select_variant(self) -> tuple[PromptTemplate, str]:
        if random.random() < self.control_weight:
            return self.control, self.control.version
        return self.variant, self.variant.version
    
    def record_result(self, version: str, score: float):
        self.results[version].append(score)
    
    def report(self) -> dict:
        stats = {}
        for v, scores in self.results.items():
            if len(scores) < 2:
                stats[v] = {"mean": 0, "n": len(scores), "significant": False}
                continue
            stats[v] = {
                "mean": statistics.mean(scores),
                "stdev": statistics.stdev(scores),
                "n": len(scores),
            }
        # t-test 簡化版本
        if len(self.results[self.control.version]) > 1 and len(self.results[self.variant.version]) > 1:
            t_stat = abs(stats[self.control.version]["mean"] - stats[self.variant.version]["mean"])
            stats["significant"] = t_stat > 0.1  # 簡化判斷
        return stats
```

## 提示詞資產管理平台

成熟的組織會建立一個 Prompt Registry 平台來管理提示詞資產，類似 Docker Hub 之於容器映像檔：

- **搜尋與發現**：團隊成員可以搜尋現有的提示詞模板
- **權限控管**：誰可以建立、修改、發布提示詞
- **審查流程**：提示詞變更需要經過 Code Review
- **發布管理**：支援金絲雀發布、藍綠部署
- **使用分析**：每個提示詞的使用次數、平均回應品質、延遲分布

```python
# Prompt Registry API 的示意
from flask import Flask, request, jsonify

app = Flask(__name__)
registry = PromptRegistry()

@app.route("/api/prompts", methods=["POST"])
def create_prompt():
    data = request.json
    prompt = PromptTemplate(**data)
    registry.register(prompt)
    return jsonify({"status": "ok", "version": prompt.version}), 201

@app.route("/api/prompts/<name>/latest", methods=["GET"])
def get_latest(name):
    prompt = registry.get_latest(name)
    if not prompt:
        return jsonify({"error": "not found"}), 404
    return jsonify({"name": prompt.name, "version": prompt.version, "template": prompt.template})

@app.route("/api/prompts/<name>/rollback/<version>", methods=["POST"])
def rollback_prompt(name, version):
    prompt = registry.rollback(name, version)
    return jsonify({"status": "ok", "version": prompt.version})
```

提示詞管理看起來像是一個工具問題，但更深層的是文化問題——當團隊開始把提示詞當作程式碼來尊重和管理時，整個 AI 開發流程的成熟度就會大幅提升。

---

**下一步**：[LLM 評估框架](focus4.md)

## 延伸閱讀

- [提示詞工程最佳實踐](https://www.google.com/search?q=prompt+engineering+best+practices)
- [Prompt Version Control Strategies](https://www.google.com/search?q=prompt+version+control+strategy)
- [A/B Testing for LLM Prompts](https://www.google.com/search?q=A+B+testing+LLM+prompts)
- [Prompt Registry Platforms](https://www.google.com/search?q=prompt+registry+platform)
