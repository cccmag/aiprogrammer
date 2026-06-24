# 深度學習與形式語言理論

## 前言

深度學習和形式語言理論似乎來自不同的時代，但現代神經網路架構的設計與形式語言理論有著深刻的聯系。循環神經網路（RNN）與正規語言理論的關係，Transformer 與上下文無關文法的類比，都是值得探索的話題。

## RNN 與正規語言

### 有限狀態機作為神經網路的原型

```python
import numpy as np

class SimpleRNN:
    """簡化 RNN，用於說明與 FSM 的關係"""
    def __init__(self, input_size, hidden_size, output_size):
        self.hidden_size = hidden_size
        # 權重矩陣
        self.Wxh = np.random.randn(hidden_size, input_size) * 0.1
        self.Whh = np.random.randn(hidden_size, hidden_size) * 0.1
        self.Why = np.random.randn(output_size, hidden_size) * 0.1
        self.bh = np.zeros((hidden_size, 1))
        self.by = np.zeros((output_size, 1))

    def forward(self, inputs):
        """前向傳播"""
        h = np.zeros((self.hidden_size, 1))

        for x in inputs:
            x = np.array(x).reshape(-1, 1)
            h = np.tanh(self.Wxh @ x + self.Whh @ h + self.bh)

        y = self.Why @ h + self.by
        return y, h

    def predict(self, inputs):
        y, _ = self.forward(inputs)
        return np.argmax(y)


def rnn_fsm_analogy():
    """
    RNN 可以被視為一種軟狀態機
    每個 hidden state 向量對應 FSM 中的一個狀態
    但與離散的 FSM 不同，RNN 的狀態是連續的
    """
    print("RNN as Soft FSM:")
    print("- Hidden state ~ FSM state")
    print("- tanh activation ~ state transition function")
    print("- Weights ~ transition rules")

rnn_fsm_analogy()
```

### RNN 的表達能力

```python
class RNNLanguageRecognizer:
    """
    使用 RNN 識別正規語言
    訓練一個 RNN 來識別 {0^n 1^n | n >= 0}
    """
    def __init__(self):
        self.rnn = SimpleRNN(input_size=1, hidden_size=8, output_size=2)

    def train(self, positive_examples, negative_examples):
        """簡化的訓練過程"""
        print("Training RNN...")
        print(f"Positive examples: {positive_examples}")
        print(f"Negative examples: {negative_examples}")

    def predict(self, sequence):
        """預測序列是否屬於語言"""
        pred = self.rnn.predict(sequence)
        return pred == 1


def rnn_expressiveness():
    print("RNN can learn some regular languages")
    print("But has difficulty with nested dependencies")
    print("Which require context-free or recursively enumerable languages")

rnn_expressiveness()
```

## LSTM 與上下文無關語言

### 棧記憶體的類比

```python
class LSTM Cell:
    """
    LSTM 的 forget gate 可以被視為一種「軟」的棧操作
    但與真正的 PDA 不同，LSTM 是連續的
    """
    def __init__(self, hidden_size):
        self.hidden_size = hidden_size

        # 輸入閘
        self.Wi = np.random.randn(hidden_size, hidden_size * 2) * 0.1
        self.bi = np.zeros((hidden_size, 1))

        # 遺忘閘
        self.Wf = np.random.randn(hidden_size, hidden_size * 2) * 0.1
        self.bf = np.zeros((hidden_size, 1))

        # 輸出閘
        self.Wo = np.random.randn(hidden_size, hidden_size * 2) * 0.1
        self.bo = np.zeros((hidden_size, 1))

        # 細胞狀態候選值
        self.Wc = np.random.randn(hidden_size, hidden_size * 2) * 0.1
        self.bc = np.zeros((hidden_size, 1))

    def forward(self, x, h_prev, c_prev):
        """LSTM 前向傳播"""
        combined = np.vstack([h_prev, x])

        i = self.sigmoid(self.Wi @ combined + self.bi)  # 輸入閘
        f = self.sigmoid(self.Wf @ combined + self.bf)  # 遺忘閘
        o = self.sigmoid(self.Wo @ combined + self.bo)  # 輸出閘
        c_tilde = np.tanh(self.Wc @ combined + self.bc)  # 細胞候選值

        c = f * c_prev + i * c_tilde  # 細胞狀態
        h = o * np.tanh(c)  # 隱藏狀態

        return h, c

    def sigmoid(self, x):
        return 1 / (1 + np.exp(-x))


def lstm_vs_pda():
    print("LSTM vs Pushdown Automata:")
    print("- Cell state ~ Stack memory (soft)")
    print("- Forget gate ~ Stack pop (soft)")
    print("- Input gate ~ Stack push (soft)")
    print("- But: continuous, not discrete")

lstm_vs_pda()
```

## Transformer 與結構化語言

### 自注意力機制

```python
def transformer_analogy():
    """
    Transformer 的 attention 機制可以被視為一種全連接的圖
    每個位置可以 attending 到任何其他位置
    這與有限狀態機的局部轉換不同
    """
    print("Transformer vs FSM:")
    print("- Self-attention: can connect any positions")
    print("- Position encoding: explicit position info")
    print("- Global context: unlike local FSM transitions")
    print("- But: fixed-size context window (practical limitation)")

transformer_analogy()
```

## 形式語言理論啟發的神經網路設計

### 神經網路文法

```python
class NeuralCFG:
    """
    基於上下文無關文法的神經網路
    使用 Neural_lstmc 來模擬棧操作
    """
    def __init__(self):
        self.lstm = LSTM Cell(hidden_size=64)
        self.stack = []

    def process(self, input_sequence):
        h = np.zeros((64, 1))
        c = np.zeros((64, 1))

        for symbol in input_sequence:
            x = np.array([[1 if symbol == '0' else 0]])
            h, c = self.lstm.forward(x, h, c)

            # 模擬基於規則的棧操作
            # 這只是一個概念示例
            if symbol == '0':
                self.stack.append(h)
            elif symbol == '1' and self.stack:
                self.stack.pop()

        return len(self.stack) == 0


def neuro_language_design():
    print("Language-inspired Neural Network Designs:")
    print("1. RNNs for regular languages")
    print("2. LSTMs/GRUs for context-free languages")
    print("3. Attention for long-range dependencies")
    print("4. Tree-LSTMs for syntactic structure")

neuro_language_design()
```

## 實證研究

### RNN 的學習能力

```python
def empirical_findings():
    """
    關於 RNN 學習形式語言能力的實證研究發現：
    """
    findings = {
        "regular": "RNN can learn regular languages with sufficient hidden units",
        "context_free": "LSTMs can learn some CFLs but not all",
        "pumping_lemma": "RNNs can learn patterns that violate pumping lemma",
        "compositionality": "Attention helps with compositional generalization",
    }

    for lang_type, finding in findings.items():
        print(f"{lang_type}: {finding}")


empirical_findings()
```

## 深度學習與喬姆斯基層級

```python
def chomsky_hierarchy_dl():
    print("Deep Learning vs Chomsky Hierarchy:")
    print("")
    print("Type 3 (Regular): RNNs, GRUs")
    print("  - Pattern matching, sequence classification")
    print("")
    print("Type 2 (Context-Free): LSTMs, Tree-LSTMs")
    print("  - Language parsing, sentiment analysis")
    print("")
    print("Type 1 (Context-Sensitive): Transformers, Neural Turing Machines")
    print("  - Long-range dependencies, memory-augmented models")
    print("")
    print("Type 0 (Unrestricted): Unknown")
    print("  - Current models are Turing complete under certain conditions")


chomsky_hierarchy_dl()
```

## 小結

深度學習與形式語言理論的結合是一個活躍的研究領域。雖然現代神經網路在許多語言任務上表現優異，但理解其與形式語言理論的聯系可以幫助我們：
1. 更好地設計網路架構
2. 理解模型的極限
3. 開發更具解釋性的 AI 系統

---

**延伸閱讀**

- [On the Computational Power of RNNs](https://www.google.com/search?q=RNN+computational+power+Turing+completeness)
- [LSTM can learn some CFLs](https://www.google.com/search?q=LSTM+context+free+language+learning)
- [Neural Network Formal Languages](https://www.google.com/search?q=neural+network+formal+language+theory)