# Do-calculus 入門：從相關到因果的關鍵一步

## 前言

2026 年的 AI 領域，「相關不等於因果」已經從教科書口號變成了工程實務的核心挑戰。Judea Pearl 的 do-calculus 提供了從觀察數據推斷因果效應的嚴謹框架——真正讓機器學會問「如果我改變 X，Y 會發生什麼變化？」

## 什麼是 Do-calculus？

Do-calculus 由 Pearl（1995）提出，是一套處理「干預」（intervention）的演算規則。傳統機率論的條件機率 P(Y|X) 描述的是「觀察到 X 時 Y 的分布」，而我們真正需要的往往是 P(Y|do(X=x))——「干預 X 為 x 時 Y 的分布」。

這兩者本質不同：觀察是被動的，干預是主動的。舉例來說，P(存活 | 吃藥) 可能受到「生病嚴重程度」的混淆；但 P(存活 | do(吃藥)) 則切斷了所有指向「吃藥」的箭頭，只保留藥物本身的因果效應。

## 三條基本規則

Do-calculus 包含三條規則，全部基於有向無環圖（DAG）的結構：

### 規則一：插入/刪除觀察

若在圖 G 中，Y 與 X 被某組變數 Z 阻斷（d-separation），則：

P(Y|do(X), Z) = P(Y|Z)

這允許我們在干預條件下省略某些觀察。

### 規則二：行動與觀察互換

若在刪除指向 X 的箭頭後的圖 G_X 中，Y 與 X 被 Z 阻斷：

P(Y|do(X), do(Z)) = P(Y|X, do(Z))

這讓干預（do）與觀察（條件）可以互換。

### 規則三：刪除干預

若在刪除指向 X 的箭頭與所有從 X 出發的箭頭後的圖 G_{XZ} 中，Y 與 X 被 Z 阻斷：

P(Y|do(X), do(Z)) = P(Y|do(Z))

這允許在特定條件下移除冗餘的干預操作。

## Python 實作：簡單的 Do-calculus 引擎

以下實作一個迷你因果圖與 do-calculus 模擬器：

```python
import itertools
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class CausalDAG:
    edges: dict[str, list[str]] = field(default_factory=dict)

    def add_edge(self, cause: str, effect: str):
        self.edges.setdefault(cause, []).append(effect)
        self.edges.setdefault(effect, [])

    def parents(self, node: str) -> list[str]:
        return [p for p, cs in self.edges.items() if node in cs]

    def children(self, node: str) -> list[str]:
        return self.edges.get(node, [])[:]

    def do(self, node: str, value: float, values: dict[str, float]) -> dict[str, float]:
        """Simulate do-calculus intervention by removing incoming edges."""
        result = values.copy()
        result[node] = value
        # Propagate through remaining structure
        topo = self._topological()
        for n in topo:
            if n == node:
                continue
            parents_vals = [result[p] for p in self.parents(n)]
            if parents_vals:
                result[n] = sum(parents_vals) / len(parents_vals)
        return result

    def _topological(self) -> list[str]:
        visited, order = set(), []
        def dfs(n):
            if n not in visited:
                visited.add(n)
                for c in self.edges.get(n, []):
                    dfs(c)
                order.append(n)
        for n in list(self.edges.keys()):
            dfs(n)
        return order


# Demo: 教育 -> 薪資，混淆：能力
dag = CausalDAG()
dag.add_edge("ability", "education")
dag.add_edge("ability", "salary")
dag.add_edge("education", "salary")

obs = {"ability": 1.0, "education": 16, "salary": 75000}
intervened = dag.do("education", 20, obs)
print(f"觀察：薪資 = {obs['salary']}")
print(f"干預 do(education=20)：薪資 = {intervened['salary']:.0f}")
```

## Do-calculus 在 XAI 中的角色

現代可解釋 AI 中，do-calculus 的應用日益廣泛：

1. **特徵歸因**：SHAP 與 LIME 本質上在回答「如果特徵 X 不同，預測會如何？」——這就是一種干預。
2. **反事實解釋**：給定一個預測結果，do-calculus 能找出最小變更特徵組合。
3. **公平性評估**：透過 do(保護屬性 = 某值) 來測量模型是否存在偏見。

## 結語

Do-calculus 不僅是因果推論的理論基石，更是建構可解釋 AI 的實用工具。從簡單的三條規則出發，它能回答傳統機器學習無法觸及的問題——「如果世界不是這樣，會發生什麼？」在下篇文章中，我們將探討 SHAP 如何將這些因果概念具體化為特徵貢獻值。

---

**延伸閱讀**
- [Judea Pearl - Causal Inference](https://www.google.com/search?q=Judea+Pearl+do+calculus+causal+inference)
- [Do-calculus 三條規則詳解](https://www.google.com/search?q=do+calculus+three+rules+pearl)
- [Causal AI with Python](https://www.google.com/search?q=causal+AI+python+do+calculus+library)
