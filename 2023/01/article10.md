# 效能評估：CPI 與 Amdahl 定律

## 1. 引言

如何客觀地評估計算機的效能？單純的時脈頻率已經不足以衡量現代處理器的真實表現。本文將介紹計算機效能評估的兩個核心工具：CPI（Cycles Per Instruction）和 Amdahl 定律。

## 2. CPU 效能公式

### 2.1 基本公式

```
CPU 時間 = 指令數 × CPI × 時脈週期時間
```

其中：
- **指令數**（Instruction Count）：程式執行的指令總數
- **CPI**：每條指令的平均時脈週期數
- **時脈週期時間**：每個時脈週期的秒數

### 2.2 公式的啟示

這個看似簡單的公式揭示了效能最佳化的三個維度：

```python
def cpu_time(inst_count, cpi, clock_rate):
    """計算 CPU 執行時間"""
    return inst_count * cpi / clock_rate

# 範例：
# 程式：10^9 條指令，CPI=1.5，時脈 3GHz
t = cpu_time(1e9, 1.5, 3e9)
print(f"執行時間: {t*1e3:.2f} ms")  # 0.5 ms
```

## 3. CPI 詳細計算

### 3.1 加權平均 CPI

不同類型的指令有不同的 CPI：

```python
class CPIAnalyzer:
    def __init__(self):
        self.inst_types = {
            'ALU':     {'count': 0, 'cpi': 1},
            'LOAD':    {'count': 0, 'cpi': 2},
            'STORE':   {'count': 0, 'cpi': 2},
            'BRANCH':  {'count': 0, 'cpi': 3},
            'FP_MUL':  {'count': 0, 'cpi': 5},
            'FP_DIV':  {'count': 0, 'cpi': 12},
        }

    def add_profile(self, itype, count):
        self.inst_types[itype]['count'] += count

    def avg_cpi(self):
        total = sum(t['count'] for t in self.inst_types.values())
        if total == 0:
            return 0
        weighted = sum(t['count'] * t['cpi'] for t in self.inst_types.values())
        return weighted / total

    def report(self):
        print("=== CPI Analysis ===")
        for name, data in self.inst_types.items():
            if data['count'] > 0:
                pct = data['count'] / sum(t['count'] for t in self.inst_types.values()) * 100
                print(f"{name:8s}: {data['count']:6d} ({pct:5.1f}%) CPI={data['cpi']}")
        print(f"Average CPI: {self.avg_cpi():.2f}")
```

### 3.2 管線對 CPI 的影響

理想管線化：CPI = 1。但冒險會導致 CPI 增加：

```
實際 CPI = 1 + 結構冒險停頓 + 資料冒險停頓 + 控制冒險停頓
```

```python
class PipelineCPI:
    def __init__(self, base_cpi=1.0):
        self.base = base_cpi
        self.data_hazard_stalls = 0.2
        self.control_hazard_stalls = 0.15
        self.structural_hazard_stalls = 0.05

    @property
    def effective_cpi(self):
        return self.base + self.data_hazard_stalls + \
               self.control_hazard_stalls + self.structural_hazard_stalls
```

## 4. Amdahl 定律

### 4.1 定律的數學表達

Amdahl 定律描述了系統效能提升的物理限制：

```
加速比 = 1 / ((1 - P) + P/S)

P = 可加速部分的比例
S = 加速倍數
```

### 4.2 定律的模擬

```python
def amdahl_speedup(P, S):
    """計算 Amdahl 加速比"""
    return 1.0 / ((1 - P) + P / S)

def amdahl_demo():
    print("=== Amdahl's Law ===")
    print("S=10 時不同 P 值的加速比：")
    for P in [0.5, 0.75, 0.9, 0.95, 0.99]:
        sp = amdahl_speedup(P, 10)
        print(f"  P={P:.2f}: speedup={sp:.2f}")

    print("\nP=0.9 時不同 S 值的加速比：")
    for S in [2, 5, 10, 20, 100]:
        sp = amdahl_speedup(0.9, S)
        print(f"  S={S:3d}: speedup={sp:.2f}")
```

### 4.3 範例執行結果

```
=== Amdahl's Law ===
S=10 時不同 P 值的加速比：
  P=0.50: speedup=1.82
  P=0.75: speedup=3.08
  P=0.90: speedup=5.26
  P=0.95: speedup=6.90
  P=0.99: speedup=9.17

P=0.9 時不同 S 值的加速比：
  S=  2: speedup=1.82
  S=  5: speedup=3.57
  S= 10: speedup=5.26
  S= 20: speedup=6.90
  S=100: speedup=9.17
```

即使將可加速部分加速 100 倍，整體加速比也只有 9.17——這是因為不可加速部分（10%）始終存在。

## 5. SPEC 基準測試

### 5.1 SPEC CPU 2017

SPEC（Standard Performance Evaluation Corporation）提供標準化的效能測試套件：

- **SPECrate**：測量吞吐量（多工場景）
- **SPECspeed**：測量單一任務的執行時間

### 5.2 基準測試的局限性

```python
def benchmark_limitations():
    """基準測試的常見問題"""
    issues = [
        "編譯器最佳化可能偏向特定基準測試",
        "單一數字無法反映所有場景的效能",
        "基準測試可能過時（不再反映實際負載）",
        "硬體配置（記憶體、儲存）影響結果",
    ]
    for issue in issues:
        print(f"- {issue}")
```

## 6. MIPS 與 MFLOPS

### 6.1 MIPS（Million Instructions Per Second）

```
MIPS = 時脈頻率 / (CPI × 10^6)
```

MIPS 的問題：不同指令集的 MIPS 不可比較（RISC 的指令比 CISC 簡單，但 MIPS 數字可能更高）。

### 6.2 MFLOPS（Million Floating-Point Operations Per Second）

MFLOPS 只計算浮點運算，在科學計算場景中更有意義：

```python
def mflops_calculation(ops_count, time_seconds):
    return ops_count / (time_seconds * 1e6)
```

## 7. 結語

效能評估沒有完美的單一指標。CPI 提供了處理器效率的微觀視角，Amdahl 定律揭示了平行化的宏觀限制，基準測試則在實際應用中驗證理論分析的結果。

對於系統設計者和軟體工程師，最重要的是理解：效能最佳化需要同時考慮演算法效率（指令數）、程式碼品質（CPI）和硬體配置（時脈頻率）。

---

**下一步**：[回顧與結語](end.md)

## 延伸閱讀

- [CPU Performance Metrics](https://www.google.com/search?q=CPU+performance+metrics+CPI+MIPS+MFLOPS)
- [SPEC Benchmark Suite](https://www.google.com/search?q=SPEC+CPU+benchmark+2017)
- [Amdahl's Law Explained](https://www.google.com/search?q=Amdahl's+law+parallel+computing+explained)
