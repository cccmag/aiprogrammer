# RNN 與上下文無關文法

## 前言

循環神經網路（RNN）與上下文無關文法（CFG）之間有著深刻的聯系。RNN 的隱藏狀態可以被視為一種廣義的棧，這使得它在處理某些 CFL 特性的任務時表現出色，但在處理完全通用的 CFL 時仍有局限。

## RNN 的棧類比

### 隱藏狀態作為棧記憶體

```python
import numpy as np

class RNNWithStackAnalogy:
    """
    RNN 的 hidden state 可以被視為一種軟棧
    每個時間步的狀態壓縮了之前的歷史資訊
    """
    def __init__(self, input_size, hidden_size):
        self.hidden_size = hidden_size
        self.W = np.random.randn(hidden_size, hidden_size) * 0.1
        self.U = np.random.randn(hidden_size, input_size) * 0.1
        self.b = np.zeros((hidden_size, 1))

    def step(self, x, h_prev):
        """單步狀態轉換"""
        h = np.tanh(self.W @ h_prev + self.U @ x + self.b)
        return h

    def process(self, sequence):
        """處理序列，狀態逐步更新"""
        h = np.zeros((self.hidden_size, 1))
        history = [h]

        for x in sequence:
            x = np.array(x).reshape(-1, 1)
            h = self.step(x, h)
            history.append(h)

        return history


def stack_analogy():
    print("RNN Hidden State as Soft Stack:")
    print("  - Continuous values, not discrete")
    print("  - Information compressed, not fully separated")
    print("  - Can approximate stack behavior")
    print("  - But: cannot simulate true PDA exactly")

stack_analogy()
```

## RNN 處理 CFL 任務

### 識別 {a^n b^n}

```python
class CounterRNN:
    """
    訓練 RNN 識別 {a^n b^n | n >= 0}
    這是典型的 CFL 語言
    """
    def __init__(self):
        self.hidden_size = 16
        self.rnn = RNNWithStackAnalogy(1, self.hidden_size)

    def train(self, positive_samples, negative_samples):
        """模擬訓練過程"""
        print("Training RNN on {a^n b^n}...")
        print(f"Positive: {positive_samples}")
        print(f"Negative: {negative_samples}")

    def predict(self, sequence):
        """預測"""
        # 簡化：根據前後部分的長度一致性判斷
        a_count = sequence.count('a')
        b_count = sequence.count('b')
        return a_count == b_count and sequence.startswith('a' * a_count + 'b' * b_count)


def counter_rnn():
    model = CounterRNN()
    tests = ['ab', 'aabb', 'aaabbb', 'aab', 'abab', 'aaaaabbbbbb']
    for t in tests:
        result = model.predict(t)
        print(f"{t}: {'Accept' if result else 'Reject'}")

counter_rnn()
```

## LSTM 與 PDA

### 更強的記憶能力

```python
class LSTMCell:
    """簡化的 LSTM 單元"""
    def __init__(self, hidden_size):
        self.hidden_size = hidden_size

        # 權重矩陣（簡化）
        self.Wf = np.random.randn(hidden_size, hidden_size * 2) * 0.1
        self.Wi = np.random.randn(hidden_size, hidden_size * 2) * 0.1
        self.Wc = np.random.randn(hidden_size, hidden_size * 2) * 0.1
        self.Wo = np.random.randn(hidden_size, hidden_size * 2) * 0.1

    def forward(self, x, h_prev, c_prev):
        """LSTM 前向傳播"""
        combined = np.vstack([h_prev, x])

        f = self.sigmoid(self.Wf @ combined)  # forget gate
        i = self.sigmoid(self.Wi @ combined)  # input gate
        c_tilde = np.tanh(self.Wc @ combined)  # cell candidate
        c = f * c_prev + i * c_tilde  # cell state

        o = self.sigmoid(self.Wo @ combined)  # output gate
        h = o * np.tanh(c)

        return h, c

    def sigmoid(self, x):
        return 1 / (1 + np.exp(-x))


class LSTMAsPDA:
    """
    LSTM 可以被視為一種更強大的狀態機
    Cell state 可以儲存更豐富的資訊
    """
    def __init__(self):
        self.hidden_size = 32
        self.lstm = LSTMCell(self.hidden_size)

    def process(self, sequence):
        """處理序列"""
        h = np.zeros((self.hidden_size, 1))
        c = np.zeros((self.hidden_size, 1))

        for symbol in sequence:
            x = np.array([[1 if symbol == 'a' else 0]])
            h, c = self.lstm.forward(x, h, c)

        return h, c


def lstm_pda():
    print("LSTM as Enhanced PDA:")
    print("  - Cell state: long-term memory")
    print("  - Forget gate: selective memory clearing")
    print("  - Input gate: selective memory adding")
    print("  - Can learn to count and remember")
    print("  - But: still not true PDA")

lstm_pda()
```

## 樹狀結構 LSTM

### 處理CFG的結構

```python
class TreeLSTM:
    """
    Tree-LSTM 可以更好地處理樹狀結構
    適合語法分析等任務
    """
    def __init__(self, hidden_size):
        self.hidden_size = hidden_size

    def forward(self, left_child, right_child):
        """處理二叉樹節點"""
        h_left, c_left = left_child
        h_right, c_right = right_child

        # 合併子節點
        h = np.tanh(np.random.randn(self.hidden_size, 1) * (h_left + h_right))
        c = c_left + c_right  # 簡化的單元更新

        return h, c


def tree_lstm():
    print("Tree-LSTM for CFG-like structures:")
    print("  - Children can be combined recursively")
    print("  - Natural fit for parse trees")
    print("  - Can model parent-child relationships")
    print("  - Better for syntactic processing")

tree_lstm()
```

## 挑戰與限制

### Pump 引理的視角

```python
def pumping_lemma_challenge():
    """
    RNN 處理需要泵浦引理的語言時會遇到困難
    因為 RNN 的狀態數有限
    """
    print("Pumping Lemma Challenge for RNNs:")
    print("")
    print("If L is context-free, it satisfies pumping lemma:")
    print("  w = uvxyz, |vxy| <= p, |vy| >= 1")
    print("  uv^i x y^i z ∈ L for all i >= 0")
    print("")
    print("RNN challenge:")
    print("  - Fixed-size hidden state")
    print("  - Cannot store unbounded 'count'")
    print("  - Relies on distributed representations")
    print("  - May approximate but not perfectly")


pumping_lemma_challenge()
```

## 實驗結果

### RNN 的 CFL 學習能力

```python
def experimental_results():
    """
    RNN 在 CFL 任務上的實驗發現
    """
    results = {
        "an_bn": "LSTM can learn with >95% accuracy",
        "an_bn_cn": "Struggles; requires more capacity",
        "palindromes": "RNNs can learn but generalize poorly",
        "balanced_parens": "LSTMs perform reasonably",
    }

    print("RNN/CFL Experimental Results:")
    for task, result in results.items():
        print(f"  {task}: {result}")

experimental_results()
```

## 小結

RNN 特別是 LSTM 在處理上下文無關語言方面展現了令人驚訝的能力。雖然從理論上講，有限狀態的 RNN 無法完美識別所有 CFL，但透過 distributed representations 和 gates 機制，LSTM 可以學習近似 CFL 的複雜模式。Tree-LSTM 更是為處理 CFG 的樹狀結構提供了自然的方式。

理解 RNN 與 CFL 的關係有助於我們選擇合適的模型架構來處理不同類型的語言任務。

---

**延伸閱讀**

- [On the Expressive Power of RNNs](https://www.google.com/search?q=expressiveness+recurrent+neural+networks+CFG)
- [LSTM Can Learn Context-Free Languages](https://www.google.com/search?q=LSTM+context+free+language+learning)
- [Neural Language Formality](https://www.google.com/search?q=neural+network+formal+language+theory)