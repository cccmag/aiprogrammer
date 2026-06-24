# AutoML：自動化機器學習

## 前言

AutoML（自動化機器學習）旨在自動化機器學習管道的各個環節，讓非專家也能使用強大的 ML 模型。

## AutoML 流程

```
機器學習流程：
────────────────────────────────

資料準備 → 特徵工程 → 模型選擇 → 超參數優化 → 部署

AutoML 自動化：
────────────────────────────────

資料準備 → 自動特徵 → 自動模型 → 自動調參 → 部署
```

## 神經架構搜尋（NAS）

```python
# NAS 示例概念

class NeuralArchitectureSearch:
    def __init__(self, search_space):
        self.search_space = search_space
    
    def sample_architecture(self):
        """從搜尋空間取樣網路架構"""
        return random.choice(self.search_space)
    
    def evaluate(self, architecture):
        """訓練並評估架構"""
        model = self.build_model(architecture)
        return train_and_evaluate(model)
    
    def search(self, num_trials=100):
        """執行搜尋"""
        best = None
        best_score = 0
        
        for _ in range(num_trials):
            arch = self.sample_architecture()
            score = self.evaluate(arch)
            
            if score > best_score:
                best = arch
                best_score = score
        
        return best
```

## 常用 AutoML 框架

| 框架 | 開發者 | 特點 |
|------|--------|------|
| AutoKeras | Keras 團隊 | 基於 Keras |
| H2O AutoML | H2O.ai | 自動化整個流程 |
| Google Cloud AutoML | Google | 雲端服務 |
| NASNet | Google | 自動化神經架構 |

## 延伸閱讀

- [AutoML 綜述](https://www.google.com/search?q=AutoML+automated+machine+learning+survey)

---

*本篇文章為「AI 程式人雜誌 2020 年 11 月號」文章集錦之一。*