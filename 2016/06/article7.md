# 神經網路作為有限狀態機

## 前言

神經網路，特別是循環神經網路（RNN），可以被理解為一種廣義的有限狀態機。本文探討神經網路狀態機的類比，以及這種理解如何幫助我們分析和改進深度學習模型。

## RNN 與 FSM 的基本類比

### 狀態的類比

```python
import numpy as np

class RNNAsFSM:
    """
    RNN 可以被視為一種狀態機
    - Hidden state: FSM 的狀態
    - Weights: 狀態轉換規則
    - Activation: 轉換函式
    """
    def __init__(self, num_states, input_size):
        self.num_states = num_states
        self.input_size = input_size

        # RNN 參數
        self.W = np.random.randn(num_states, num_states) * 0.1
        self.U = np.random.randn(num_states, input_size) * 0.1
        self.b = np.zeros((num_states, 1))

    def transition(self, x, h_prev):
        """狀態轉換"""
        h = np.tanh(self.W @ h_prev + self.U @ x + self.b)
        return h

    def run_sequence(self, inputs):
        """處理序列"""
        h = np.zeros((self.num_states, 1))
        states = [h]

        for x in inputs:
            x = np.array(x).reshape(-1, 1)
            h = self.transition(x, h)
            states.append(h)

        return states


def rnn_as_fsm():
    print("RNN as FSM:")
    print("  - Hidden state = FSM state")
    print("  - Weight matrix = transition function")
    print("  - Non-linearity = allows soft, continuous transitions")

rnn_as_fsm()
```

## 狀態可解釋性

### 離散化隱藏狀態

```python
def discretize_states():
    """
    將 RNN 的連續狀態離散化為離散的 FSM 狀態
    """
    def cluster_states(hidden_states, num_clusters):
        """使用 k-means 離散化"""
        from sklearn.cluster import KMeans

        states_array = np.array(hidden_states).squeeze()
        kmeans = KMeans(n_clusters=num_clusters, random_state=0).fit(states_array)
        return kmeans.labels_

    print("Discretizing continuous states:")
    print("  - Cluster hidden states")
    print("  - Map to discrete labels")
    print("  - Analyze state transitions")
    print("  - Extract finite state machine")


discretize_states()
```

## 實際應用

### 語音辨識中的聲學狀態

```python
class AcousticStateMachine:
    """
    簡化的語音辨識狀態機
    每個狀態對應一個語音單元
    """
    def __init__(self):
        self.states = {
            'sil': {'phone': 'sil', 'next': ['ah', 'eh', 'iy']},
            'ah': {'phone': 'AH', 'next': ['l', 'r', 'sil']},
            'eh': {'phone': 'EH', 'next': ['l', 'r', 'sil']},
            'iy': {'phone': 'IY', 'next': ['l', 'r', 'sil']},
            'l': {'phone': 'L', 'next': ['ah', 'eh', 'iy', 'sil']},
            'r': {'phone': 'R', 'next': ['ah', 'eh', 'iy', 'sil']},
        }
        self.current = 'sil'

    def transition(self, observation):
        """根據觀測轉換狀態"""
        # 簡化：隨機轉換
        import random
        possible = self.states[self.current]['next']
        self.current = random.choice(possible)

    def get_phoneme(self):
        return self.states[self.current]['phone']


def acoustic_fsm():
    model = AcousticStateMachine()
    phones = []
    for _ in range(20):
        model.transition(None)
        phones.append(model.get_phoneme())
    print(f"Generated phoneme sequence: {phones}")

acoustic_fsm()
```

### 文字生成中的 RNN 狀態機

```python
class CharRNN:
    """
    字元級 RNN 可以被視為字符狀態機
    """
    def __init__(self, vocab):
        self.vocab = vocab
        self.char_to_idx = {c: i for i, c in enumerate(vocab)}
        self.idx_to_char = {i: c for i, c in enumerate(vocab)}

        # 簡化的 RNN
        self.hidden_size = 50
        self.W = np.random.randn(self.hidden_size, self.hidden_size) * 0.1
        self.U = np.random.randn(self.hidden_size, len(vocab)) * 0.1
        self.V = np.random.randn(len(vocab), self.hidden_size) * 0.1

    def forward(self, chars):
        """前向傳播"""
        h = np.zeros((self.hidden_size, 1))

        for char in chars:
            x = np.zeros((len(self.vocab), 1))
            x[self.char_to_idx[char]] = 1
            h = np.tanh(self.W @ h + self.U @ x)

        y = self.V @ h
        return y

    def generate(self, seed, length):
        """生成文字"""
        result = seed
        h = np.zeros((self.hidden_size, 1))

        for _ in range(length):
            x = np.zeros((len(self.vocab), 1))
            x[self.char_to_idx[result[-1]]] = 1
            h = np.tanh(self.W @ h + self.U @ x)

            y = self.V @ h
            probs = np.exp(y) / np.sum(np.exp(y))
            next_idx = np.random.choice(len(self.vocab), p=probs.ravel())
            result += self.idx_to_char[next_idx]

        return result


def char_rnn_fsm():
    vocab = list("abcdefghijklmnopqrstuvwxyz ")
    rnn = CharRNN(vocab)
    print("Character RNN as Character-level FSM")

char_rnn_fsm()
```

## 狀態機視角下的訓練

### 課程學習

```python
def curriculum_learning():
    """
    從簡單狀態機到複雜狀態機的課程學習
    """
    print("Curriculum Learning as State Machine Building:")
    print("  Stage 1: Learn simple patterns (few states)")
    print("  Stage 2: Add more complex patterns (more states)")
    print("  Stage 3: Fine-tune transitions")
    print("  Similar to building up a complex FSM from simple ones")


curriculum_learning()
```

## 網路架構與狀態複雜度

```python
def state_complexity():
    """網路容量與可表示狀態數的關係"""
    print("Network Capacity vs State Complexity:")
    print("")
    print("Hidden size h:")
    print("  - Can represent up to 2^h distinct states")
    print("  - More hidden units = more distinguishable states")
    print("")
    print("Number of layers:")
    print("  - Increases representational depth")
    print("  - Allows state composition")
    print("")
    print("Recurrent connections:")
    print("  - Enable temporal state evolution")
    print("  - Like FSM state transitions over time")


state_complexity()
```

## 長期依賴問題

```python
def long_term_dependencies():
    """
    RNN 的長期依賴問題可以被理解為狀態機的狀態丟失
    隨著序列增長，早期的狀態資訊被稀釋
    """
    print("Long-term Dependencies as State Decay:")
    print("")
    print("Problem:")
    print("  - RNN state has limited capacity")
    print("  - Early state info gets overwritten")
    print("  - Like an FSM with states that forget history")
    print("")
    print("Solutions:")
    print("  - LSTMs/GRUs: gated state updates (selective memory)")
    print("  - Attention: directly connect to earlier states")
    print("  - Memory augmentation: external state storage")


long_term_dependencies()
```

## 實際分析工具

### 神經網路狀態可視化

```python
def state_visualization():
    """將 RNN 狀態可視化為狀態機"""
    print("Visualizing RNN as FSM:")
    print("")
    print("1. Extract hidden states for many inputs")
    print("2. Cluster/embed states in 2D space")
    print("3. Identify state transitions")
    print("4. Visualize as graph")
    print("")
    print("Tools: t-SNE, UMAP, PCA for visualization")
    print("Libraries: NetV.js, TensorBoard")


state_visualization()
```

## 小結

將神經網路視為廣義的狀態機為我們提供了一個有用的分析視角。RNN 的 hidden state 可以類比為 FSM 的狀態，weight matrices 類比為轉換函式。這種觀點幫助我們：
1. 理解網路的表達能力
2. 診斷訓練問題
3. 設計更好的架構

---

**延伸閱讀**

- [Neural State Machine](https://www.google.com/search?q=neural+state+machine)
- [RNN as Finite State Machine](https://www.google.com/search?q=RNN+finite+state+machine+analogy)
- [Visualizing RNN Hidden States](https://www.google.com/search?q=visualizing+RNN+hidden+states)