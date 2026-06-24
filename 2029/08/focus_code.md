# 程式實作：量子 ML 示範

## 簡介

本實作從零建構量子 ML 模擬器，展示量子位元操作、變分量子電路和量子核方法。完整程式碼在 `_code/quantum_ml.py`。

## 核心元件

### 1. 量子位元

```python
q = Qubit()
q.apply_hadamard()
q.apply_pauli_x()
result = q.measure()
```

### 2. 變分量子電路

```python
circuit = VariationalCircuit(4)
params = [0.5, 1.2, 0.8, 0.3]
output = circuit.run(params)
```

### 3. 量子核方法

```python
kernel = QuantumKernel()
similarity = kernel.compute(state1, state2)
```

## 執行方式

```bash
cd _code
python3 quantum_ml.py
```

## 延伸練習

1. **VQE 實作**：用量子電路解決最佳化問題
2. **量子 SVM**：實現量子核支援向量機
3. **混合訓練**：串接 PyTorch 進行混合訓練
4. **更多量子閘**：加入 CNOT、Toffoli 閘
5. **真實量子硬體**：用 Qiskit 連接 IBM 量子處理器
