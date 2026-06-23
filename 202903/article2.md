# 提示詞管理系統設計

## 前言

提示詞（Prompt）是 AI 原生應用的核心資產。缺乏系統化管理會導致版本混亂、難以追蹤、協作困難。本文介紹如何設計提示詞管理系統。

## 版本管理

### 儲存結構

```python
from pydantic import BaseModel
from datetime import datetime
from typing import Optional
import hashlib

class PromptTemplate(BaseModel):
    id: str
    name: str
    version: int
    content: str
    variables: list[str]
    hash: str = ""
    created_at: datetime = datetime.now()
    updated_at: datetime = datetime.now()

    def compute_hash(self) -> str:
        return hashlib.sha256(self.content.encode()).hexdigest()

class PromptRepository:
    def __init__(self):
        self._templates: dict[str, list[PromptTemplate]] = {}

    def save(self, template: PromptTemplate) -> PromptTemplate:
        template.hash = template.compute_hash()
        template.version = len(self._templates.get(template.name, [])) + 1
        self._templates.setdefault(template.name, []).append(template)
        return template

    def get_latest(self, name: str) -> Optional[PromptTemplate]:
        versions = self._templates.get(name, [])
        return versions[-1] if versions else None

    def get_version(self, name: str, version: int) -> Optional[PromptTemplate]:
        versions = self._templates.get(name, [])
        return versions[version - 1] if 0 < version <= len(versions) else None
```

### 模板渲染

```python
from string import Template

class PromptRenderer:
    def __init__(self, repo: PromptRepository):
        self.repo = repo

    async def render(self, name: str, variables: dict) -> str:
        template = self.repo.get_latest(name)
        if not template:
            raise ValueError(f"Prompt {name} not found")

        missing = [v for v in template.variables if v not in variables]
        if missing:
            raise ValueError(f"Missing variables: {missing}")

        return Template(template.content).safe_substitute(variables)

prompt_repo = PromptRepository()

prompt_repo.save(PromptTemplate(
    id="summary-v1",
    name="summary",
    content="請總結以下文章，字數限制在 ${max_words} 字內：\n\n${text}",
    variables=["max_words", "text"]
))
```

## A/B 測試支援

```python
import random

class PromptExperiment:
    def __init__(self, repo: PromptRepository):
        self.repo = repo

    async def render_with_traffic(self, name: str, variables: dict) -> tuple[str, str]:
        versions = self.repo._templates.get(name, [])
        if len(versions) < 2:
            template = versions[0]
            return self.render_template(template, variables), template.version

        weights = [0.5] * len(versions)
        template = random.choices(versions, weights=weights)[0]
        return self.render_template(template, variables), template.version

    def render_template(self, template: PromptTemplate, variables: dict) -> str:
        return Template(template.content).safe_substitute(variables)
```

## 監控與稽核

```python
import logging

class PromptAuditor:
    def __init__(self):
        self.logger = logging.getLogger("prompt_audit")

    def log_call(self, template_name: str, version: int, variables: dict, response: str):
        self.logger.info({
            "event": "prompt_call",
            "template": template_name,
            "version": version,
            "variables": variables,
            "response_length": len(response),
        })

auditor = PromptAuditor()
```

## 結語

提示詞管理系統應支援版本控制、模板渲染、A/B 測試和稽核日誌。將提示詞視為程式碼一樣管理，才能確保 AI 應用行為的一致性和可追溯性。

---

**延伸閱讀**

- [Prompt Engineering 指南](https://www.google.com/search?q=prompt+engineering+best+practices)
- [提示詞版本管理](https://www.google.com/search?q=prompt+version+management)
- [LLM 提示詞優化工具](https://www.google.com/search?q=LLM+prompt+optimization+tools)
