# Lambda Calculus 在現代 AI 中的重生（2010s-2020s）

## 深度學習的函式視角

2012 年，AlexNet 在 ImageNet 競賽中取得突破性成果，標誌著深度學習時代的來臨。從那時起，我們可以從一個獨特的角度看待深度學習：

**神經網路本質上是一個巨大的複合函式。**

```python
# 深度學習模型就是函式組合
# 輸入 -> 線性層 -> 激活函式 -> 線性層 -> 激活函式 -> ... -> 輸出

class NeuralNetwork(nn.Module):
    def __init__(self):
        super().__init__()
        self.layers = nn.Sequential(
            nn.Linear(784, 256),
            nn.ReLU(),
            nn.Linear(256, 128),
            nn.ReLU(),
            nn.Linear(128, 10)
        )
    
    def forward(self, x):
        return self.layers(x)

# 這就是一個巨大的函式
# f(x) = W3 * ReLU(W2 * ReLU(W1 * x + b1) + b2) + b3
# 或者用 Lambda Calculus 的視角：
# f = λx. (W3 (ReLU (W2 (ReLU (W1 x + b1)) + b2)) + b3)
```

---

## 函式視角的深度學習

### 層的組合

在函式視角下，每個神經網路層都是一個函式：

```python
import torch.nn.functional as F

# 線性變換：矩陣乘法
linear = lambda x, W, b: W @ x + b

# 激活函式
relu = lambda x: torch.maximum(x, torch.zeros_like(x))

# Softmax
softmax = lambda x: torch.exp(x) / torch.exp(x).sum(dim=-1, keepdim=True)

# 組合這些函式
layer1 = lambda x: relu(linear(x, W1, b1))
layer2 = lambda x: relu(linear(x, W2, b2))
output = lambda x: softmax(linear(x, W3, b3))

# 完整網路
network = lambda x: output(layer2(layer1(x)))
```

### 自動微分：梯度計算的自動化

```python
# PyTorch 的自動微分
x = torch.tensor([1.0, 2.0], requires_grad=True)
y = x ** 2 + 2 * x + 1  # y = x^2 + 2x + 1

# 計算梯度
y.sum().backward()

# 結果：dy/dx = 2x + 2 = [4, 6]
print(x.grad)  # tensor([4., 6.])
```

### 函式式 API

現代深度學習框架提供了函式式的模型建構 API：

```python
# Keras Functional API
inputs = tf.keras.Input(shape=(28, 28, 1))
x = layers.Conv2D(32, 3, activation='relu')(inputs)
x = layers.MaxPooling2D(2)(x)
x = layers.GlobalAveragePooling2D()(x)
outputs = layers.Dense(10)(x)
model = tf.keras.Model(inputs, outputs)

# 視為函式組合
# model = Dense(10) ∘ GAP ∘ MaxPool ∘ Conv2D ∘ Input

# JAX：純函式_transform
import jax
import jax.numpy as jnp

@jax.jit  # 編譯加速
@jax.grad  # 自動梯度
def loss(params, x, y):
    pred = forward(params, x)
    return cross_entropy_loss(pred, y)
```

---

## Transformer 架構與注意力機制

2017 年，Google 發表了革命性的論文《Attention Is All You Need》。這個 Transformer 架構現在是幾乎所有大型語言模型的基礎。

### 從函式程式設計的角度理解 Transformer

```python
# 注意力機制的函式視角
def attention(query, keys, values):
    """
    注意力機制的核心思想：
    
    1. query: 查詢函式（我們想要查什麼）
    2. keys: 鍵（每個位置的標識）
    3. values: 值（每個位置的內容）
    
    輸出是 values 的加權和，權重由 query 和 keys 的相似度決定
    
    這本質上是一個高階函式！
    """
    # 計算相似度（點積）
    scores = torch.matmul(query, keys.transpose(-2, -1))
    
    # 標準化
    scores = scores / math.sqrt(keys.size(-1))
    
    # Softmax 權重
    weights = F.softmax(scores, dim=-1)
    
    # 加權求和
    return torch.matmul(weights, values)
```

### 多頭注意力：並行的多個注意力函式

```python
class MultiHeadAttention(nn.Module):
    def __init__(self, d_model, num_heads):
        super().__init__()
        self.num_heads = num_heads
        self.d_k = d_model // num_heads
        
        # 四個線性變換（函式）
        self.W_q = nn.Linear(d_model, d_model)
        self.W_k = nn.Linear(d_model, d_model)
        self.W_v = nn.Linear(d_model, d_model)
        self.W_o = nn.Linear(d_model, d_model)
    
    def forward(self, query, key, value, mask=None):
        batch_size = query.size(0)
        
        # 線性變換（函式應用）
        Q = self.W_q(query)
        K = self.W_k(key)
        V = self.W_v(value)
        
        # 分頭（函式的分割）
        Q = Q.view(batch_size, -1, self.num_heads, self.d_k).transpose(1, 2)
        K = K.view(batch_size, -1, self.num_heads, self.d_k).transpose(1, 2)
        V = V.view(batch_size, -1, self.num_heads, self.d_k).transpose(1, 2)
        
        # 並行注意力計算（map）
        x, attn_weights = attention(Q, K, V)
        
        # 合併頭（函式的合併）
        x = x.transpose(1, 2).contiguous().view(batch_size, -1, self.num_heads * self.d_k)
        
        return self.W_o(x)
```

### 視覺化注意力

```
┌─────────────────────────────────────────────────────┐
│               注意力機制示意                          │
├─────────────────────────────────────────────────────┤
│                                                     │
│   Query: "機器學習" ──────┐                        │
│                            │                        │
│   ┌───────────────────────▼───────────────────┐    │
│   │            注意力計算                       │    │
│   │  scores = Q @ K^T / sqrt(d_k)            │    │
│   │  weights = softmax(scores)               │    │
│   │  output = weights @ V                     │    │
│   └───────────────────────┬───────────────────┘    │
│                            │                        │
│   Keys: [機器, 學習, 是, 什麼]                    │
│   Values: [機器, 學習, 是, 什麼]                   │
│                            │                        │
│                            ▼                        │
│   輸出：加權組合的上下文表示                        │
│                                                     │
└─────────────────────────────────────────────────────┘
```

---

## AI Agent 與函式呼叫

2023 年後，AI Agent 成為熱門話題。其核心思想是：讓 AI 模型呼叫外部工具和函式。這正是 Lambda Calculus「應用」概念的現代詮釋。

### 函式呼叫的現代形態

```python
# AI Agent 呼叫外部函式
class Agent:
    def __init__(self, llm, tools):
        self.llm = llm
        self.tools = {t.name: t for t in tools}
    
    async def execute(self, query: str):
        # LLM 規劃並選擇工具
        plan = await self.llm.plan(query, available_tools=list(self.tools.keys()))
        
        results = []
        for step in plan:
            tool_name = step["tool"]
            params = step["parameters"]
            
            # 函式應用
            if tool_name in self.tools:
                result = await self.tools[tool_name].call(**params)
                results.append(result)
            else:
                raise ValueError(f"Unknown tool: {tool_name}")
        
        # 最終響應
        return await self.llm.synthesize(query, results)
```

### 工具定義與註冊

```python
from typing import TypedDict, List

# 定義工具
class Tool:
    def __init__(self, name: str, description: str, parameters: dict):
        self.name = name
        self.description = description
        self.parameters = parameters
    
    async def call(self, **kwargs):
        # 工具實現
        pass

# 計算路線
calculate_route = Tool(
    name="calculate_route",
    description="計算兩地之間的路線",
    parameters={
        "type": "object",
        "properties": {
            "origin": {"type": "string"},
            "destination": {"type": "string"}
        },
        "required": ["origin", "destination"]
    }
)

# 搜尋資料庫
search_database = Tool(
    name="search_database",
    description="搜尋資料庫",
    parameters={
        "type": "object",
        "properties": {
            "query": {"type": "string"},
            "filters": {"type": "object"}
        },
        "required": ["query"]
    }
)

# 使用
agent = Agent(llm, [calculate_route, search_database])
response = await agent.execute("從台北到高雄的最短路徑是什麼？")
```

### OpenAI 的函式呼叫

```python
# OpenAI 的函式呼叫 API
tools = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "獲取指定城市的天氣資訊",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "城市名稱"
                    }
                },
                "required": ["location"]
            }
        }
    }
]

response = openai.chat.completions.create(
    model="gpt-5",
    messages=[{"role": "user", "content": "台北今天天氣如何？"}],
    tools=tools
)

# 解析函式呼叫
tool_calls = response.choices[0].message.tool_calls
for call in tool_calls:
    if call.function.name == "get_weather":
        args = json.loads(call.function.arguments)
        weather = get_weather(location=args["location"])
```

---

## 向量化與函式抽象

在深度學習中，向量化是將函式應用於整個資料結構的過程——這與函式程式設計的「映射」概念完全一致。

### 向量化的概念

```python
import numpy as np

# 傳統方式：迴圈
def add_matrices_slow(A, B):
    C = np.zeros_like(A)
    for i in range(A.shape[0]):
        for j in range(A.shape[1]):
            C[i, j] = A[i, j] + B[i, j]
    return C

# 向量化方式：函式應用於整個結構
def add_matrices_fast(A, B):
    return A + B  # NumPy 的廣播機制

# 這正是函式程式設計中的 map！
# map(add, zip(A, B))
```

### 張量運算的函式視角

```python
import torch

# 張量運算本質上是函式
x = torch.randn(32, 128, 768)  # [batch, seq, hidden]

# 所有操作都是函式
h = F.layer_norm(x, (768,))           # 層歸一化
h = F.dropout(h, p=0.1)              # Dropout
h = F.gelu(h)                         # 激活函式

# 這些都是純函式！
# h = gelu(dropout(layer_norm(x)))
```

### PyTorch 的函式式設計

```python
# Sequential：函式組合
model = nn.Sequential(
    nn.Linear(784, 256),
    nn.ReLU(),
    nn.Linear(256, 128),
    nn.ReLU(),
    nn.Linear(128, 10)
)

# forward 方法本質上是函式組合
# model(x) = W3(ReLU(W2(ReLU(W1(x)))))

# Functional API
from torch.nn import functional as F

def forward(x, weights):
    x = F.linear(x, weights['w1'], weights['b1'])
    x = F.relu(x)
    x = F.linear(x, weights['w2'], weights['b2'])
    return x
```

---

## 大語言模型的本質

從 Lambda Calculus 的視角看，大語言模型（LLM）可以被理解為一個巨大的函式：

```python
# LLM 本質上是一個從文字到文字的函式
llm = lambda input_text: model.generate(input_text)

# 這與 Lambda Calculus 的函式應用完全一致：
# (λx.M) N  → M[x := N]

# 現代 LLM 的函式特性
class LLM:
    def __call__(self, text: str) -> str:
        # 這是一個從 str -> str 的函式
        return self.generate(text)
    
    def generate(self, text: str) -> str:
        # 內部是複雜的張量運算
        ...
```

### Transformer 的函式視角

```
┌─────────────────────────────────────────────────────┐
│               Transformer = 函式組合                  │
├─────────────────────────────────────────────────────┤
│                                                     │
│  Transformer(input) =                              │
│      LayerNorm(                                   │
│          MultiHeadAttention(                       │
│              LayerNorm(input)                      │
│          ) + input                                 │
│      )                                             │
│      LayerNorm(                                    │
│          FeedForward(                              │
│              LayerNorm(...)                        │
│          ) + ...                                   │
│      )                                             │
│      ... × N 層                                    │
│      Linear(..., vocab_size)                       │
│                                                     │
│  這就是一個巨大的組合函式！                         │
│                                                     │
└─────────────────────────────────────────────────────┘
```

---

## 未來展望：AI 與函式編程的融合

### 當前的趨勢

1. **AI 輔助編程**：AI 能夠理解和生成函式程式碼
2. **形式化驗證**：借助 AI 證明程式的正確性
3. **自動優化**：AI 幫助優化函式組合

### 未來可能的方向

```python
# 可能的未來：AI 自動生成最佳函式組合
optimized_model = auto_optimize(
    model,
    objective="minimize_latency",
    constraints=["accuracy > 0.95"]
)

# 或：AI 輔助的形式化證明
proof = ai_prove(
    theorem="所有偶數的平方是 4 的倍數",
    strategy="mathematical_induction"
)
```

### 函式視角的價值

從函式視角理解 AI 有幾個優勢：

1. **更清晰的推理**：函式組合比矩陣運算更容易理解
2. **更好的優化**：識別可以組合或分解的函式
3. **更安全的 AI**：形式化方法可以用於 AI 安全分析

---

## 結語

從 1936 年的 Lambda Calculus，到 2026 年的 Transformer，我們看到了一個美麗的循環：

- **Church 的抽象**：λx.M（建立函式）
- **Church 的應用**：M N（應用函式）
- **現代的組合**：Transformer 的層層堆疊

神經網路本質上是在學習一個巨大的複合函式，而 AI Agent 的函式呼叫正是 Lambda Calculus「應用」概念的現代實現。

在這個 AI 迅速發展的時代，讓我們記住這些基本概念。因為無論技術如何變遷，抽象和組合的威力永遠不會過時。

---

## 延伸閱讀

- [Vaswani 2017: Attention Is All You Need](https://www.google.com/search?q=Attention+Is+All+You+Need+Transformer)
- [深度學習與函式編程](https://www.google.com/search?q=deep+learning+functional+programming)
- [AI Agent 技術](https://www.google.com/search?q=AI+agent+function+calling)

---

*本篇文章為「AI 程式人雜誌 2026 年 3 月號」歷史回顧系列之七。*
