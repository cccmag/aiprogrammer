"""
分散式訓練模擬 — DataParallel, ModelParallel, 梯度累積, ZeRO 最佳化
純 CPU 可執行，不依賴 PyTorch
"""

import numpy as np
from typing import List, Callable

# ---------- 資料平行 (DataParallel) ----------
class DataParallelSim:
    """模擬多 worker 資料平行：每 worker 拿到不同 batch"""
    def __init__(self, n_workers: int):
        self.n_workers = n_workers

    def scatter(self, data: np.ndarray) -> List[np.ndarray]:
        return np.array_split(data, self.n_workers)

    def sync_gradients(self, grads: List[np.ndarray]) -> np.ndarray:
        return sum(grads) / len(grads)


# ---------- 模型平行 (ModelParallel) ----------
class ModelParallelSim:
    """模擬模型平行：不同層放在不同裝置"""
    def __init__(self, n_stages: int, input_dim: int, hidden_dim: int):
        self.n_stages = n_stages
        self.weights = [np.random.randn(hidden_dim, hidden_dim) * 0.01
                        for _ in range(n_stages)]
        self.biases = [np.zeros(hidden_dim) for _ in range(n_stages)]

    def forward(self, x: np.ndarray, stage: int) -> np.ndarray:
        return x @ self.weights[stage] + self.biases[stage]


# ---------- 梯度累積 (Gradient Accumulation) ----------
class GradientAccumulator:
    """累積多步梯度後才更新參數，模擬大 batch"""
    def __init__(self, accum_steps: int = 4):
        self.accum_steps = accum_steps
        self.buffer: List[np.ndarray] = []
        self.step = 0

    def add_gradient(self, grad: np.ndarray) -> np.ndarray | None:
        self.buffer.append(grad)
        self.step += 1
        if self.step % self.accum_steps == 0:
            averaged = sum(self.buffer) / len(self.buffer)
            self.buffer.clear()
            return averaged
        return None


# ---------- ZeRO 最佳化模擬 ----------
class ZeROOptimizer:
    """模擬 ZeRO Stage 1: 最佳化器狀態分散到各 worker"""
    def __init__(self, params: List[np.ndarray], n_workers: int):
        self.params = params
        self.n_workers = n_workers
        self.m = [np.zeros_like(p) for p in params]
        self.v = [np.zeros_like(p) for p in params]
        self.worker_id = 0

    def assign_worker(self, wid: int):
        """每個 worker 只負責一部分參數"""
        self.worker_id = wid
        per_worker = len(self.params) // self.n_workers
        start = wid * per_worker
        end = start + per_worker if wid < self.n_workers - 1 else len(self.params)
        self.owned = list(range(start, end))

    def step(self, grads: List[np.ndarray], lr: float = 0.01):
        for i in self.owned:
            self.m[i] = 0.9 * self.m[i] + 0.1 * grads[i]
            self.v[i] = 0.999 * self.v[i] + 0.001 * grads[i] ** 2
            m_hat = self.m[i] / (1 - 0.9)
            v_hat = self.v[i] / (1 - 0.999)
            self.params[i] -= lr * m_hat / (np.sqrt(v_hat) + 1e-8)
        return [self.params[i] for i in self.owned]


# ---------- 整合示範 ----------
def demo():
    print("=" * 50)
    print("分散式訓練模擬 (Distributed Training Simulation)")
    print("=" * 50)

    # 1. DataParallel 示範
    print("\n[1] DataParallel 資料平行")
    dp = DataParallelSim(n_workers=4)
    data = np.random.randn(32, 64)
    shards = dp.scatter(data)
    print(f"  原始資料 shape: {data.shape}")
    print(f"  分片後每 worker: {shards[0].shape} x {len(shards)} workers")

    # 模擬各 worker 計算梯度
    local_grads = [np.random.randn(64) for _ in range(4)]
    synced = dp.sync_gradients(local_grads)
    print(f"  梯度同步後 shape: {synced.shape}")

    # 2. ModelParallel 示範
    print("\n[2] ModelParallel 模型平行")
    mp = ModelParallelSim(n_stages=3, input_dim=64, hidden_dim=64)
    x = np.random.randn(8, 64)
    for s in range(mp.n_stages):
        x = mp.forward(x, s)
        print(f"  Stage {s+1} 輸出 shape: {x.shape}")

    # 3. 梯度累積示範
    print("\n[3] Gradient Accumulation 梯度累積")
    acc = GradientAccumulator(accum_steps=4)
    for step in range(8):
        grad = np.random.randn(64)
        result = acc.add_gradient(grad)
        if result is not None:
            print(f"  第 {step+1} 步: 累積完成，平均梯度 shape = {result.shape}")
        else:
            print(f"  第 {step+1} 步: 累積中...")

    # 4. ZeRO 最佳化示範
    print("\n[4] ZeRO Optimizer (Stage 1)")
    params = [np.random.randn(16) for _ in range(8)]
    zero = ZeROOptimizer(params, n_workers=4)
    for wid in range(4):
        zero.assign_worker(wid)
        grads = [np.random.randn(16) for _ in range(8)]
        updated = zero.step(grads, lr=0.01)
        print(f"  Worker {wid}: 更新 {len(updated)} 組參數")

    print("\n" + "=" * 50)
    print("示範完成 — 所有模擬均在 CPU 上執行")
    print("=" * 50)


if __name__ == "__main__":
    demo()
