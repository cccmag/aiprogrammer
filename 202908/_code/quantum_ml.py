"""
量子 ML 模擬器 — 變分量子電路、量子核、混合架構
"""
import math
import random
import cmath
from dataclasses import dataclass, field

class Qubit:
    def __init__(self):
        self.alpha = 1.0 + 0j
        self.beta = 0.0 + 0j
    def apply_hadamard(self):
        self.alpha, self.beta = (self.alpha + self.beta) / math.sqrt(2), (self.alpha - self.beta) / math.sqrt(2)
    def apply_pauli_x(self):
        self.alpha, self.beta = self.beta, self.alpha
    def measure(self) -> int:
        prob0 = abs(self.alpha)**2
        return 0 if random.random() < prob0 else 1

class QuantumCircuit:
    def __init__(self, n_qubits: int = 2):
        self.qubits = [Qubit() for _ in range(n_qubits)]
    def hadamard(self, q: int): self.qubits[q].apply_hadamard()
    def cx(self, control: int, target: int):
        if self.qubits[control].measure() == 1:
            self.qubits[target].apply_pauli_x()
    def measure_all(self) -> list[int]: return [q.measure() for q in self.qubits]

class VariationalQuantumCircuit(QuantumCircuit):
    def __init__(self, n_qubits: int = 2):
        super().__init__(n_qubits)
        self.params = [random.uniform(0, 2*math.pi) for _ in range(n_qubits)]
    def forward(self, x: list[float]) -> list[int]:
        for i, q in enumerate(self.qubits):
            angle = sum(x) * self.params[i] if x else self.params[i]
            q.alpha = math.cos(angle / 2) + 0j
            q.beta = math.sin(angle / 2) + 0j
        return self.measure_all()

class QuantumKernel:
    def similarity(self, x: list[float], y: list[float]) -> float:
        dot = sum(a * b for a, b in zip(x, y))
        return math.exp(-0.5 * (1 - dot / (math.sqrt(sum(a*a for a in x)) * math.sqrt(sum(b*b for b in y)) + 1e-10)))

def demo():
    print("=== Quantum ML Simulator ===\n")
    qc = QuantumCircuit(2)
    qc.hadamard(0)
    qc.cx(0, 1)
    print(f"  Bell state measurement: {qc.measure_all()}")
    vqc = VariationalQuantumCircuit(2)
    print(f"  VQC params: {[round(p, 2) for p in vqc.params]}")
    print(f"  VQC output: {vqc.forward([1.0, 0.5])}")
    kernel = QuantumKernel()
    sim = kernel.similarity([1, 0], [0.8, 0.6])
    print(f"  Quantum kernel similarity: {sim:.4f}")
    print("\n=== Demo Complete ===")

if __name__ == "__main__":
    demo()
