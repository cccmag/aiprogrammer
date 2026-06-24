# 提示詞版本控制：Git + Registry 雙層管理

## 前言

2027 年的 AI 工程團隊已經普遍接受一個原則：**提示詞就是程式碼**。如同原始碼需要 Git 管理，提示詞同樣需要版本控制、差異比對、審查流程和發布管理。但提示詞的版本控制比程式碼更複雜——同一個提示詞的不同版本可能同時在線上運行（A/B 測試），而且提示詞的品質評估不像編譯器報錯那麼明確。

本文提出一個實戰驗證過的雙層架構：**Git 層**管理變更歷史與協作流程，**Registry 層**管理運行時版本與發布策略。

## 第一層：Git 管理提示詞變更

最直接的方式是將提示詞以結構化格式存放在 Git 儲存庫中：

```
prompts/
├── summaries/
│   ├── v1.0.0.yaml       # 初始版本
│   ├── v1.1.0.yaml       # 加入格式要求
│   └── v2.0.0.yaml       # 改為 Chain-of-Thought 架構
├── classifications/
│   ├── v1.0.0.yaml
│   └── v2.0.0.yaml
└── agents/
    ├── customer_service/
    │   ├── v1.0.0.yaml
    │   └── v1.1.0.yaml
    └── data_analyst/
        └── v1.0.0.yaml
```

每個提示詞檔案採用結構化格式：

```yaml
# prompts/summaries/v2.0.0.yaml
name: article_summarizer
version: 2.0.0
author: alice@example.com
created_at: 2027-06-15
description: 使用 Chain-of-Thought 的多步驟摘要提示詞

parameters:
  - name: article
    type: string
    description: 要摘要的文章內容

template: |
  你是一個專業的技術文章摘要專家。

  請按照以下步驟進行摘要：

  1. **分析**：找出文章的核心論點與關鍵證據
  2. **組織**：將資訊按重要性排序
  3. **濃縮**：用不超過三句話呈現

  文章：
  {article}

  摘要：

tests:
  - input:
      article: "機器學習是一種人工智慧的子領域..."
    expected_output_contains: ["機器學習", "人工智慧"]
    max_tokens: 200
  - input:
      article: ""
    expected_error: "article 不可為空"
```

### Git 的 Diff 在提示詞上的應用

```python
# 提示詞差異比較工具
import yaml
import difflib

class PromptDiffer:
    def compare_versions(self, v1_path: str, v2_path: str) -> dict:
        with open(v1_path) as f:
            v1 = yaml.safe_load(f)
        with open(v2_path) as f:
            v2 = yaml.safe_load(f)

        changes = {
            "metadata_diff": self._diff_metadata(v1, v2),
            "template_diff": self._diff_text(v1["template"], v2["template"]),
            "parameters_diff": self._diff_params(
                v1.get("parameters", []),
                v2.get("parameters", [])
            ),
            "tests_changed": v1.get("tests", []) != v2.get("tests", [])
        }

        # 計算語義影響分數（簡化版）
        changes["impact_score"] = self._calculate_impact(changes)
        return changes

    def _diff_text(self, old: str, new: str) -> list[dict]:
        differ = difflib.unified_diff(
            old.splitlines(), new.splitlines(),
            lineterm=""
        )
        changes = []
        for line in differ:
            if line.startswith("+") or line.startswith("-"):
                changes.append(line)
        return changes

    def _calculate_impact(self, changes: dict) -> float:
        score = 0.0
        if changes["template_diff"]:
            score += 0.6  # 模板變更影響最大
        if changes["parameters_diff"]:
            score += 0.3
        if changes["tests_changed"]:
            score += 0.1
        return min(score, 1.0)
```

## 第二層：Registry 運行時管理

Git 管理版本歷史，但無法直接支援 A/B 測試和漸進式發布。Registry 層負責運行時的版本管理：

```python
# 提示詞 Registry 的生產級實作
from datetime import datetime
from typing import Optional
import json

class PromptVersion:
    def __init__(self, name: str, version: str, template: str,
                 params: list[str], hash: str):
        self.name = name
        self.version = version
        self.template = template
        self.params = params
        self.hash = hash  # SHA256 of template
        self.deployed_at: Optional[datetime] = None
        self.rollback_count: int = 0

class PromptRegistry:
    def __init__(self, storage_backend: str = "redis"):
        self.versions: dict[str, list[PromptVersion]] = {}
        self.active: dict[str, PromptVersion] = {}  # 當前活躍版本
        self.deployment_history: list[dict] = []

    def register_from_git(self, yaml_path: str) -> PromptVersion:
        """從 Git 管理的 YAML 檔案註冊到 Registry"""
        import hashlib
        import yaml

        with open(yaml_path) as f:
            data = yaml.safe_load(f)

        template_hash = hashlib.sha256(
            data["template"].encode()
        ).hexdigest()[:12]

        version = PromptVersion(
            name=data["name"],
            version=data["version"],
            template=data["template"],
            params=[p["name"] for p in data.get("parameters", [])],
            hash=template_hash
        )

        if data["name"] not in self.versions:
            self.versions[data["name"]] = []
        self.versions[data["name"]].append(version)

        return version

    def deploy(self, name: str, version: str,
               strategy: str = "immediate") -> dict:
        """部署特定版本的提示詞"""
        target = None
        for v in self.versions.get(name, []):
            if v.version == version:
                target = v
                break

        if not target:
            return {"status": "error", "message": f"Version {version} not found"}

        deployment = {
            "name": name,
            "version": version,
            "strategy": strategy,
            "timestamp": datetime.now().isoformat(),
            "status": "deploying"
        }

        if strategy == "immediate":
            self.active[name] = target
            target.deployed_at = datetime.now()
            deployment["status"] = "deployed"

        elif strategy == "canary":
            canary_config = {
                "control": self.active.get(name),
                "variant": target,
                "canary_percent": 5,
                "monitoring_window": "24h"
            }
            deployment["canary"] = canary_config
            # 實際的金絲雀發布由另一個服務處理
            deployment["status"] = "canary_started"

        self.deployment_history.append(deployment)
        return deployment

    def rollback(self, name: str) -> Optional[PromptVersion]:
        """回滾到前一個版本"""
        versions = self.versions.get(name, [])
        if len(versions) < 2:
            return None

        current = self.active.get(name)
        current_idx = -1
        for i, v in enumerate(versions):
            if v.version == current.version:
                current_idx = i
                break

        if current_idx > 0:
            prev = versions[current_idx - 1]
            prev.rollback_count += 1
            self.active[name] = prev
            self.deployment_history.append({
                "action": "rollback",
                "name": name,
                "from": current.version,
                "to": prev.version,
                "timestamp": datetime.now().isoformat()
            })
            return prev
        return None

    def get_deployment_report(self, name: str) -> dict:
        """取得部署報告"""
        versions = self.versions.get(name, [])
        return {
            "name": name,
            "total_versions": len(versions),
            "active_version": self.active.get(name).version if self.active.get(name) else None,
            "deployment_count": len(self.deployment_history),
            "rollback_rate": sum(
                1 for v in versions if v.rollback_count > 0
            ) / max(len(versions), 1),
            "last_deployed": versions[-1].deployed_at.isoformat() if versions and versions[-1].deployed_at else None
        }
```

## 與 CI/CD 整合

提示詞的版本管線應該與 CI/CD 系統整合：

```yaml
# .github/workflows/prompt-cd.yaml (GitHub Actions)
name: Prompt CD
on:
  push:
    paths:
      - 'prompts/**/*.yaml'

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Validate prompt files
        run: python scripts/validate_prompts.py
      - name: Run prompt tests
        run: python scripts/test_prompts.py

  deploy-staging:
    needs: validate
    runs-on: ubuntu-latest
    steps:
      - name: Deploy to staging registry
        run: |
          python scripts/register_prompts.py \
            --env staging \
            --git-ref ${{ github.sha }}

  deploy-production:
    needs: deploy-staging
    runs-on: ubuntu-latest
    environment: production
    steps:
      - name: Canary deploy to production
        run: |
          python scripts/canary_deploy.py \
            --percent 5 \
            --monitor-h 24
```

## 實戰建議

1. **Commit 訊息規範**：`prompt(summarizer): 加入 COT 架構改善摘要品質 (#123)`
2. **每次變更都要測試**：至少包含格式驗證和關鍵詞檢查
3. **部署前必須 Code Review**：提示詞變更需要至少一位同事審查
4. **記錄 Rollback 原因**：每次回退都記錄原因，累積成團隊知識庫
5. **定期清理舊版本**：保留最近 N 個版本和所有 Production 版本即可

## 參考資源

- [Prompt Version Control Strategies](https://www.google.com/search?q=prompt+version+control+strategy+2027)
- [Git + Registry 雙層管理架構](https://www.google.com/search?q=prompt+registry+git+dual+layer)
- [提示詞 CI/CD 最佳實踐](https://www.google.com/search?q=prompt+CI+CD+best+practices)
- [OpenAI Prompt Management Guide](https://www.google.com/search?q=OpenAI+prompt+management+best+practices)
