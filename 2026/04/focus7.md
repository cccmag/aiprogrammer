# AI 時代的編譯器：機器學習輔助最佳化與 AI 編譯器（2020s）

## 機器學習與編譯器的交會

2020 年代，機器學習開始深刻改變編譯器的設計和實現。這種改變體現在兩個方向：

1. **ML for Compilers**：用機器學習改進傳統編譯器的最佳化決策
2. **Compilers for ML**：為深度學習模型設計專用的編譯器

## ML for Compilers：機器學習輔助的最佳化

傳統編譯器的最佳化決策依賴於手工編寫的啟發式規則（Heuristics）。這些規則雖然經過精心設計，但往往無法適應所有情況。機器學習提供了一種自動學習最佳化策略的方法。

### 啟發式規則的局限

```
// 傳統的內聯啟發式（GCC）
bool should_inline(Function *callee, CallSite *cs) {
    // 簡單的規則：
    if (callee->size() < 10)    return true;   // 小函式，一定內聯
    if (callee->size() > 1000)  return false;  // 大函式，一定不內聯
    if (cs->is_hot() && callee->size() < 100) return true;  // 熱點
    if (callee->has_loops())    return false;  // 有迴圈，不內聯
    // ... 還有數十條規則
    return default_heuristic();  
}

// 問題：
// - 規則之間可能互相衝突
// - 手動調整閾值非常耗時
// - 可能對特定硬體或應用不是最優的
```

### MLGO：機器學習引導的最佳化

Google 的 MLGO（Machine Learning Guided Optimization）專案將強化學習應用於編譯器最佳化。

```
MLGO 的訓練流程：

          ┌─────────────────────┐
          │    訓練資料收集      │
          │  (大量原始碼、基準)  │
          └──────────┬──────────┘
                     │
                     ▼
          ┌─────────────────────┐
          │  ML 模型訓練        │
          │  (強化學習)         │
          └──────────┬──────────┘
                     │
                     ▼
          ┌─────────────────────┐
          │  訓練好的模型        │
          │  (策略網路)          │
          └──────────┬──────────┘
                     │
                     ▼
          ┌─────────────────────┐
          │  將模型嵌入 LLVM     │
          │  替換啟發式規則      │
          └──────────┬──────────┘
                     │
                     ▼
          ┌─────────────────────┐
          │  編譯時使用 ML 決策  │
          │  決定內聯、暫存器分配│
          └─────────────────────┘
```

**具體應用：內聯決策（Inlining）**

```python
# MLGO 的內聯決策模型（簡化示意）
class InliningPolicy:
    def __init__(self):
        self.model = load_policy_model()
    
    def should_inline(self, caller, callee, context):
        # 提取特徵
        features = {
            'caller_size': caller.num_instructions(),
            'callee_size': callee.num_instructions(),
            'call_depth': context.depth,
            'hotness': context.invoke_count,
            'has_loops': callee.has_loops(),
            'num_callsites': callee.num_call_sites(),
            'returns_void': callee.returns_void(),
            'allocates_memory': callee.allocates(),
            # ... 數十個特徵
        }
        
        # 神經網路決策
        score = self.model.predict(features)
        
        # 返回機率（是否需要內聯）
        return score > 0.5
```

MLGO 的效果：
- 在 SPEC CPU 基準測試中，效能提升 2-5%
- 程式碼大小減少 3-8%
- 自動適應不同的硬體平台和工作負載

### 自動化搜尋的編譯器最佳化

除了內聯，機器學習還被應用於：

1. **迴圈展開因數選擇**：展開多少倍最合適？
2. **向量化決策**：哪些迴圈應該 SIMD 向量化？
3. **暫存器分配順序**：哪個變數應該優先分配到暫存器？
4. **指令排程策略**：如何排序指令以減少流水線停頓？
5. **垃圾收集時機**：何時觸發 GC 最合適？

## Compilers for ML：深度學習模型專用編譯器

### 為什麼需要 AI 專用編譯器？

深度學習模型與傳統程式有很大差異：

```
傳統程式 vs 深度學習模型：

傳統程式：控制流密集
  if (cond) {
      for (i = 0; i < n; i++) {
          x = a[i] + b[i];
      }
  }

深度學習模型：計算密集、資料流密集
  // 一個典型的 Transformer 層
  x = LayerNorm(x)
  x = MultiHeadAttention(x, x, x) + x
  x = LayerNorm(x)
  x = FeedForward(x) + x

// 深度學習模型的特性：
// - 大量矩陣乘法（GEMM）
// - 有限的控制流
// - 巨大的計算圖
// - 多種硬體目標（GPU, TPU, NPU）
```

### MLIR：多層級中間表示

MLIR（Multi-Level Intermediate Representation）是 LLVM 專案的一個子專案，旨在為深度學習編譯提供靈活的基礎設施。

```
MLIR 的多層級設計：

┌─────────────────────────────────────────────────────┐
│              MLIR 層級結構                           │
├─────────────────────────────────────────────────────┤
│                                                     │
│  高層 IR（TensorFlow Graph, PyTorch Module）       │
│  ┌─────────────────────────────────────────────┐   │
│  │ tf.Add, tf.MatMul, torch.conv2d             │   │
│  └──────────────────┬──────────────────────────┘   │
│                     │    降級 (Dialect Conversion)  │
│                     ▼                               │
│  ┌─────────────────────────────────────────────┐   │
│  │ Linalg (線性代數操作)                       │   │
│  │ linalg.matmul, linalg.conv                  │   │
│  └──────────────────┬──────────────────────────┘   │
│                     │    降級                       │
│                     ▼                               │
│  ┌─────────────────────────────────────────────┐   │
│  │ Affine + SCF (仿射變換 + 結構化控制流)      │   │
│  └──────────────────┬──────────────────────────┘   │
│                     │    降級                       │
│                     ▼                               │
│  ┌─────────────────────────────────────────────┐   │
│  │ LLVM IR (LLVM 標準後端)                     │   │
│  └──────────────────┬──────────────────────────┘   │
│                     │    程式碼生成                 │
│                     ▼                               │
│              GPU/CPU/TPU/NPU 機器碼                │
└─────────────────────────────────────────────────────┘
```

MLIR 引入了「Dialect」（方言）的概念——每一層 IR 都是一種 Dialect：

```mlir
// MLIR 範例：一個簡單的張量運算

// 高層：Linalg Dialect
#map = affine_map<(m, n, k) -> (m, k)>
#map1 = affine_map<(m, n, k) -> (k, n)>
#map2 = affine_map<(m, n, k) -> (m, n)>

func @matmul(%a: tensor<128x64xf32>, 
             %b: tensor<64x32xf32>) -> tensor<128x32xf32> {
  %c = linalg.matmul ins(%a, %b: tensor<128x64xf32>, tensor<64x32xf32>)
                        outs(%init: tensor<128x32xf32>)
  return %c : tensor<128x32xf32>
}

// 降級到 LLVM Dialect 後：
// 循環嵌套 + 向量化指令
// 最終生成高效的 GPU kernel 或 CPU 程式碼
```

### XLA：Google 的深度學習編譯器

XLA（Accelerated Linear Algebra）是 Google 為 TensorFlow/PyTorch 開發的深度學習編譯器。

```
XLA 的編譯流程：

PyTorch/TensorFlow 計算圖
      │
      ▼
┌─────────────────────┐
│  XLA HLO            │  High-Level Optimizer
│  (高階 IR)          │  - 運算融合
└──────────┬──────────┘  - 常量傳播
           │             - 死運算消除
           ▼
┌─────────────────────┐
│  XLA LHLO           │  Low-Level Optimizer
│  (低階 IR)          │  - 記憶體規劃
└──────────┬──────────┘  - 並行化
           │             - 資料複製最佳化
           ▼
┌─────────────────────┐
│  後端               │
│  CPU / GPU / TPU    │
└─────────────────────┘
```

**運算融合（Operation Fusion）**：

XLA 的最大特色之一是運算融合——將多個小運算合併為一個大 kernel：

```python
# PyTorch 中的多個運算
def layer(x, w, b):
    t1 = torch.matmul(x, w)     # GEMM
    t2 = torch.add(t1, b)       # 加法
    t3 = torch.relu(t2)         # 激活函式
    return t3

# 無 XLA：三個獨立的 GPU kernel 啟動
# 1. GEMM kernel    (大量資料從記憶體→GPU→記憶體)
# 2. Add kernel     (大量資料從記憶體→GPU→記憶體)
# 3. ReLU kernel    (大量資料從記憶體→GPU→記憶體)

# 有 XLA：融合為一個 kernel
# 1. Fused kernel  (資料只在 GPU 暫存器中流動！)
#    計算 pattern: max(0, x @ w + b)
```

融合的好處：
- 減少記憶體頻寬消耗（減少中間結果的讀寫）
- 減少 kernel 啟動開銷
- 提高算術強度（compute-to-memory ratio）

### TVM：Apache 深度學習編譯器

TVM（Tensor Virtual Machine）是另一個重要的深度學習編譯器：

```
TVM 架構：

┌─────────────────────────────────────────────┐
│  前端                                        │
│  Relay IR (高階中間表示)                    │
│  ┌──────────────────────────────────────┐   │
│  │ 自動微分、型別推論、量化             │   │
│  └──────────────────┬───────────────────┘   │
│                     ▼                       │
│  TIR (張量中間表示)                       │
│  ┌──────────────────────────────────────┐   │
│  │ 迴圈變換、張量化、記憶體管理         │   │
│  └──────────────────┬───────────────────┘   │
│                     ▼                       │
│  自動調優 (AutoTVM)                       │
│  ┌──────────────────────────────────────┐   │
│  │ 使用 ML 搜尋最佳排程                  │   │
│  └──────────────────┬───────────────────┘   │
│                     ▼                       │
│  後端                                       │
│  LLVM / CUDA / OpenCL / Vulkan             │
└─────────────────────────────────────────────┘
```

TVM 的自動調優：

```python
# TVM AutoTVM 範例
import tvm
from tvm import te
from tvm import auto_scheduler

# 定義矩陣乘法
N = 1024
A = te.placeholder((N, N), name='A')
B = te.placeholder((N, N), name='B')
k = te.reduce_axis((0, N), name='k')
C = te.compute((N, N), lambda i, j: te.sum(A[i, k] * B[k, j], axis=k))

# 自動搜尋最佳排程
task = auto_scheduler.SearchTask(func=C, args=(A, B, C))
tune_option = auto_scheduler.TuningOptions(
    num_measure_trials=1000,
    measure_callbacks=[auto_scheduler.RecordToFile('log.json')]
)
task.tune(tune_option)

# 使用找到的最佳排程
sch, args = task.apply_best('log.json')
module = tvm.build(sch, args)
```

TVM 使用機器學習（如 XGBoost 或遺傳演算法）來搜尋最佳排程策略。

## 自動微分與編譯器

自動微分（Automatic Differentiation, AD）是深度學習的基石。編譯器在自動微分中扮演著關鍵角色。

### 前向模式與反向模式

```python
# 前向模式自動微分
def forward_ad(f, x, dx):
    # 同時計算 f(x) 和 f'(x) * dx
    # 適合輸入少、輸出多的情況
    pass

# 反向模式自動微分（最常用於深度學習）
def reverse_ad(f, x):
    # 先計算 f(x)，再反向傳播梯度
    # 適合輸入多、輸出少的情況（如神經網路）
    pass
```

### 編譯器在自動微分中的角色

現代自動微分框架（如 PyTorch 2.0 的 TorchScript 和 `torch.compile`）將自動微分視為編譯器問題：

```python
import torch

# PyTorch 2.0 的編譯模式
@torch.compile
def model(x, w, b):
    return torch.relu(x @ w + b)

# torch.compile 的內部工作流程：
# 1. 追蹤計算圖（Trace）
# 2. 降級為中間表示（TorchDynamo IR）
# 3. 應用編譯器最佳化（融合、消除死代碼）
# 4. 生成反向模式的自動微分函式
# 5. 編譯為 Triton kernel 或 CUDA 程式碼
```

## 編譯器開發的 AI 輔助

### 大語言模型與編譯器

2024-2026 年間，大語言模型開始被應用於編譯器開發本身：

1. **編譯器 Pass 生成**：用 LLM 生成編譯器最佳化 pass 的原始碼
2. **IR 分析**：用 LLM 分析 LLVM IR 並提出最佳化建議
3. **除錯輔助**：用 LLM 分析編譯錯誤訊息並提供修復建議
4. **文件生成**：自動生成編譯器 pass 的文件和註釋

```python
# 示意：用 LLM 輔助編譯器最佳化
prompt = """
分析以下 LLVM IR，找出可以應用的最佳化：

define i32 @add(i32 %a, i32 %b) {
  %1 = add i32 %a, 0
  %2 = add i32 %1, %b
  ret i32 %2
}

建議最佳化：________________
"""

# LLM 回覆：
# 1. 常量摺疊：%1 = add i32 %a, 0 → %a
# 2. 簡化：直接返回 ret i32 add i32 %a, %b
```

### 未來的編譯器設計

展望未來，AI 與編譯器的融合可能帶來：

1. **完全自適應的編譯器**：根據目標硬體和工作負載自動調整策略
2. **整模型最佳化**：從演算法到機器碼的端到端最佳化
3. **自我學習的編譯器**：在實際部署中不斷學習和改進
4. **人機協作編譯器**：開發者用自然語言指定最佳化目標，編譯器自動實作

## 結語

AI 時代的編譯器正在經歷一場雙向革命：機器學習不僅在改進傳統編譯器的每個角落，深度學習還催生了全新類別的編譯器。MLIR、XLA、TVM 等系統正在重新定義什麼是「編譯器」。

從 1940 年代的打孔卡，到 1957 年的 FORTRAN 編譯器，再到 2026 年的 AI 輔助編譯器——這八十年的演進告訴我們：編譯器技術從未停止進化，而 AI 正在將它帶入一個全新的時代。

---

## 延伸閱讀

- [MLGO: Machine Learning Guided Optimization](https://www.google.com/search?q=MLGO+Google+compiler+optimization)
- [MLIR: Multi-Level IR](https://www.google.com/search?q=MLIR+multi+level+intermediate+representation)
- [XLA: Accelerated Linear Algebra](https://www.google.com/search?q=XLA+TensorFlow+compiler)
- [TVM: Tensor Virtual Machine](https://www.google.com/search?q=TVM+Apache+deep+learning+compiler)

---

*本篇文章為「AI 程式人雜誌 2026 年 4 月號」歷史回顧系列之七。*
