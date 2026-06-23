# AI 應用安全設計（2024-2029）

## 別讓你的 AI 被騙

### 前言

2024 年，Prompt Injection 攻擊還是新鮮事。2029 年，AI 應用的攻擊面已經涵蓋提示詞注入、資料中毒、模型逆向和供應鏈攻擊。安全必須是 AI 原生架構的內建元件。

### Prompt Injection（2024-2025）

最早的攻擊手法——讓模型忽略原始指令：

```python
# 2024：基礎注入防護
def safe_prompt(system_prompt, user_input):
    sanitized = sanitize_input(user_input)
    sanitized = strip_delimiters(sanitized)
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": sanitized},
    ]
    return llm(messages)
```

但簡單過濾很快被繞過——攻擊者發明了編碼、分詞、角色扮演等變體。

### 分層防禦（2025-2027）

業界建立多層防護架構：

```python
# 2026：分層安全
class SecurityLayer:
    async def process(self, user_input):
        # L1：輸入過濾
        if self.input_guard.detect_injection(user_input):
            return "請求被拒絕"

        # L2：權限隔離
        response = await self.isolated_llm.call(user_input)

        # L3：輸出驗證
        if self.output_guard.detect_leak(response):
            response = self.redact(response)

        # L4：審計日誌
        self.audit_log.record(user_input, response)
        return response
```

### 資料安全與隔離（2026-2028）

RAG 應用引入了新的資料安全挑戰：

```python
# 2027：安全 RAG
class SecureRAG:
    async def query(self, user, question):
        access_level = self.auth.get_level(user)
        results = await self.vector_db.search(
            question,
            filter={"access": {"$lte": access_level}}
        )
        return await self.llm.generate(results, question)
```

向量資料庫需要行層級的存取控制。

### 供應鏈安全（2028-2029）

AI 應用的供應鏈攻擊日益嚴重：

```python
# 2029：供應鏈驗證
class SecureModelLoader:
    def load(self, model_name):
        manifest = self.registry.verify(model_name)
        if not manifest.signature_valid:
            raise SecurityError("模型簽章無效")
        model = self.download(manifest.url)
        assert hash(model) == manifest.sha256
        return model
```

### 小結

AI 應用的安全從單一輸入過濾進化為分層防禦、資料隔離、供應鏈驗證的完整體系。**安全不是後加的功能，而是從架構第一天就必須考慮的元件**。

---

**下一步**：[AI 原生應用的未來](focus7.md)

## 延伸閱讀

- [Prompt Injection Prevention](https://www.google.com/search?q=prompt+injection+prevention+LLM+security)
- [LLM Application Security](https://www.google.com/search?q=LLM+application+security+best+practices+2025)
- [AI Supply Chain Security](https://www.google.com/search?q=AI+supply+chain+security+model+verification)
