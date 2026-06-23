# 程式碼生成模型架構（2020-2028）

## 從語言模型到程式碼模型

2020 年，OpenAI 發布了 GPT-3，證明了大型語言模型（LLM）在自然語言生成上的驚人能力。但 GPT-3 的程式碼生成能力有限——它在網頁文本上訓練，程式碼只是其中的一小部分。

關鍵問題：程式碼和自然語言有什麼不同？

```
自然語言：模糊、上下文依賴、容忍錯誤
程式碼：精確、語法嚴格、語義唯一

程式碼生成的要求：
- 100% 語法正確
- 符合型別系統
- 邏輯正確
- 安全可靠
```

## Codex：程式碼專用的 GPT

2021 年，OpenAI 發布了 Codex——GPT-3 在大量 GitHub 程式碼上微調的版本。Codex 的架構本質上是 Decoder-only Transformer：

```
輸入：def fibonacci(n):"""計算費氏數列"""
      ↓  Token Embedding + Positional Encoding
      ↓  12 層 Transformer Decoder（自注意力 + FFN）
      ↓  輸出機率分布 → 採樣 → 下一個 token
```

## 2023：指令微調與 RLHF

2023 年，InstructGPT / ChatGPT 的指令微調（Instruction Tuning）徹底改變了程式碼生成：

```python
# 指令微調的訓練格式
prompt = """
人類：寫一個 Python 函式，接收一個列表並返回所有偶數的平方。
AI："""
# 模型學會了理解自然語言指令

# RLHF 進一步優化
def rlhf_training():
    # SFT：監督微調
    sft_model = supervised_finetune(base_model, human_demo)
    # RM：獎勵模型訓練
    reward_model = train_reward_model(human_preferences)
    # PPO：強化學習優化
    final_model = ppo_optimize(sft_model, reward_model)
```

RLHF 的關鍵是學習人類的偏好——開發者喜歡簡潔、可讀、正確的程式碼，而不是冗長或含有安全漏洞的程式碼。

## 2024：Fill-in-the-Middle（FIM）

標準語言模型只能從左到右生成。FIM 技術使用特殊 sentinel tokens 讓模型可以填空：

```
<fim_prefix>def process_data(data):
    <fim_suffix>
    return result
<fim_middle>result = []
for item in data: result.append(item * 2)
```

這讓 IDE 中的「補全中間」成為可能。

## 2025：Repo-level 上下文建模

模型不再只看當前檔案，而是理解整個倉庫——跨檔案的型別引用、函式調用和設計模式：

```python
class RepoContextEncoder:
    def encode(self, repo):
        embeddings = [self.file_encoder(f.read()) for f in repo.files]
        graph = build_dependency_graph(repo)
        return self.repo_graph(embeddings, graph)
```

## 2026-2028：Agentic Code Generation

2026 年後的模型從「單次生成」轉向「迭代式生成」：

```python
def agentic_generate(spec):
    plan = model.plan(spec)        # 規劃步驟
    for step in plan:
        code = model.generate(step)  # 生成代碼
        feedback = run_tests(code)   # 執行測試
        if feedback.failed:
            code = model.revise(code, feedback)  # 根據反饋修改
    return code
```

## 延伸閱讀

- [GPT-3 Language Models are Few-Shot Learners](https://www.google.com/search?q=GPT-3+language+model+2020)
- [Codex Evaluating Large Language Models Trained on Code](https://www.google.com/search?q=OpenAI+Codex+2021)
- [Training Language Models to Follow Instructions](https://www.google.com/search?q=InstructGPT+RLHF+2022)
- [Fill-in-the-Middle for Code Completion](https://www.google.com/search?q=Fill+in+the+Middle+code+completion+FIM)

---

*本篇文章為「AI 程式人雜誌 2028 年 1 月號」主題系列之二。*
