# 提示詞管理與版本控制（2023-2029）

## 提示詞也是程式碼

### 前言

2023 年，提示詞還是工程師在 Playground 裡手動調參的文字片段。2029 年，提示詞已經是經過版本控制、CI/CD 測試、A/B 測試的正式資產。

### 手動時代（2023-2024）

最早的提示詞管理是「複製貼上」：

```python
# 2023：提示詞散落在程式碼各處
def translate(text):
    # 從 Slack 複製來的提示詞
    return llm(f"請將以下翻譯成英文：{text}")

def summarize(text):
    # 從 Notion 筆記複製來的提示詞
    return llm(f"請用三句話總結：{text}")
```

每次修改都需要手動測試，沒有版本追蹤，改壞了只能憑記憶回退。

### 模板化時代（2024-2025）

開發者開始用模板引擎管理提示詞：

```python
# 2024：提示詞模板
from jinja2 import Template

PROMPTS = {
    "translate": Template(
        "你是專業翻譯。請將 {source_lang} 翻譯成 {target_lang}：\n{text}"
    ),
    "summarize": Template(
        "請用 {style} 風格總結以下內容（{max_words} 字內）：\n{text}"
    ),
}
```

提示詞有了結構，但仍然和程式碼存放在一起，缺乏獨立的版本歷史。

### Git 管理提示詞（2025-2027）

團隊開始將提示詞存放在獨立檔案中，納入 Git 版本控制：

```python
# 2025：從 YAML 載入提示詞
import yaml

with open("prompts/translate.yaml") as f:
    config = yaml.safe_load(f)

response = llm(config["prompt"].format(text=text))
```

```yaml
# prompts/translate.yaml
version: 1.2.0
model: gpt-4o
prompt: "你是專業翻譯。請翻譯成{target_lang}：{text}"
tests:
  - input: { text: "Hello", target_lang: "中文" }
    expected: "你好"
```

提示詞有了版本、測試和模型綁定。

### 提示詞生命週期管理（2028-2029）

2028 年後，完整的提示詞管理流程出現：

```python
# 2028：提示詞生命週期
class PromptManager:
    def deploy(self, name, version):
        prompt = self.registry.get(name, version)
        if self.a_b_test(prompt):
            self.rollout(prompt)
            self.monitor_latency_and_quality()
            return "deployed"

    def rollback(self, name):
        prev = self.registry.previous(name)
        self.activate(prev)
```

### 小結

提示詞管理從散落程式碼到獨立資產、從手動測試到 CI/CD、從固定版本到 A/B 測試，最終成為完整的生命週期管理流程。

---

**下一步**：[RAG 整合最佳實踐](focus3.md)

## 延伸閱讀

- [Prompt Version Control Best Practices](https://www.google.com/search?q=prompt+version+control+best+practices+2025)
- [Prompt Management Tools 2025](https://www.google.com/search?q=prompt+management+tools+2024+2025)
- [Prompt Testing and CI/CD](https://www.google.com/search?q=prompt+testing+CI+CD+pipeline)
