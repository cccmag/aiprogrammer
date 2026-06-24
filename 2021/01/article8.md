# 多任務學習與元學習

## 多任務學習

### 概念

多任務學習（Multi-Task Learning）同時訓練模型完成多個任務：

```python
# 多任務學習範例
tasks = ["分類", "翻譯", "摘要"]

for task in tasks:
    output = model(input, task=task)
    loss = task_loss(output, task)
    loss.backward()
```

### 優勢

1. **共享表示**：相關任務互相增強
2. **泛化能力**：學習更通用的特徵
3. **效率**：一次訓練，多種能力

## 元學習（Meta-Learning）

### Learn to Learn

元學習旨在讓模型學會「如何學習」：

```
傳統學習：給定任務 → 學習技能
元學習：多個任務 → 學會學習方法
```

### MAML 算法

Model-Agnostic Meta-Learning (MAML)：
- 學習的良好初始參數
- 快速適應新任務

## 與大型語言模型的關聯

GPT-3 的 Few-shot 能力可視為一種元學習：
- 從少量範例快速推斷任務
- 無需梯度更新

---

## 延伸閱讀

- [多任務學習介紹](https://www.google.com/search?q=multi-task+learning+deep+learning)
- [MAML+算法詳解](https://www.google.com/search?q=MAML+model-agnostic+meta-learning)
- [元學習+ Few-shot](https://www.google.com/search?q=meta-learning+few-shot+GPT-3)

*本篇文章為「AI 程式人雜誌 2021 年 1 月號」精選文章。*