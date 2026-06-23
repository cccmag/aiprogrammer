# 評估的未來趨勢

## 1. 從靜態到動態評估

傳統基準使用固定資料集，容易過度擬合與資料污染。未來評估將轉向動態生成——由 AI 自動產生新題目，確保模型無法透過記憶作答。

```python
def dynamic_eval(model, generator, rounds=100):
    scores = []
    for _ in range(rounds):
        question = generator.generate(model.domain)
        answer = generator.gold_answer(question)
        prediction = model(question)
        scores.append(answer == prediction)
    return statistics.mean(scores)
```

## 2. 個人化評估

同一模型在不同使用者場景中表現各異。未來趨勢是根據目標使用情境建立個人化評估任務，而非追求單一排行榜分數。

## 3. 自動化評估代理

AI 評估代理能自主設計實驗、執行測試並撰寫報告。這不僅提升效率，還能發現人類未預期到的失敗模式。

## 4. 多 Agent 評估生態

不同評估框架之間的互操作性將成為重點。標準化的評估介面（如 LM Eval Harness 的 task 格式）促進生態系統的協作與共享。

## 5. 法規驅動的評估

歐盟 AI Act、美國 AI 行政命令要求特定風險等級的模型進行註冊與評估。合規評估將從自願變為強制，推動評估標準化進程。

## 6. 結語

評估的未來在於自動化、個人化與標準化。隨著 AI 能力持續提升，評估不再只是開發後的驗收環節，而是貫穿整個生命週期的核心機制。誰能掌握評估，誰就能掌握 AI 的發展方向。

- https://www.google.com/search?q=dynamic+benchmark+LLM+evaluation+future
- https://www.google.com/search?q=EU+AI+Act+model+evaluation+requirements
