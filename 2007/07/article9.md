# 演化式計算：遺傳演算法的實際應用

## 概述

演化式計算（Evolutionary Computation）是模擬自然演化原理的計算方法，包含遺傳演算法、演化策略、遺傳程式設計等。2007 年，這些技術在最佳化、機器學習、遊戲 AI 等領域有著廣泛應用。

## 遺傳演算法基礎

### 核心概念

遺傳演算法模擬自然選擇和遺傳機制：

```
初始化群體 → 評估適應度 → 選擇 → 交配 → 突變 → 下一代
     ↑                                                          |
     └──────────────────────────────────────────────────────────┘
```

### 基本組成

1. **染色體（Chromosome）** -- 可能的解決方案
2. **基因（Gene）** -- 解決方案的組成部分
3. **族群（Population）** -- 一組染色體
4. **適應度函數（Fitness Function）** -- 評估解決方案的好壞
5. **選擇（Selection）** -- 選優秀個體
6. **交配（Crossover）** -- 重組產生新個體
7. **突變（Mutation）** -- 隨機改變基因

## Python 實作

```python
"""
遺傳演算法 Python 實作
解決經典的函數最佳化問題
"""

import random
import math

def demo():
    print("=" * 50)
    print("遺傳演算法展示")
    print("=" * 50)

    # 問題：最大化 f(x) = sin(x) * x/10 在區間 [0, 20]
    print("\n--- 問題定義 ---")
    print("目標：最大化 f(x) = sin(x/10) * x")
    print("搜尋範圍：[0, 20]")

    # 參數設定
    POPULATION_SIZE = 50
    GENERATIONS = 100
    MUTATION_RATE = 0.1
    CROSSOVER_RATE = 0.8
    GENE_LENGTH = 16

    def fitness(x):
        """適應度函數"""
        result = math.sin(x / 10) * x
        return max(0, result)  # 確保非負

    def decode(chromosome):
        """將二進制染色體解碼為實數"""
        value = int(chromosome, 2)
        return (value / (2**GENE_LENGTH - 1)) * 20

    def create_chromosome():
        """建立隨機染色體"""
        return ''.join(random.choice('01') for _ in range(GENE_LENGTH))

    def crossover(parent1, parent2):
        """單點交配"""
        if random.random() < CROSSOVER_RATE:
            point = random.randint(1, GENE_LENGTH - 1)
            child1 = parent1[:point] + parent2[point:]
            child2 = parent2[:point] + parent1[point:]
            return child1, child2
        return parent1, parent2

    def mutate(chromosome):
        """位元翻轉突變"""
        result = list(chromosome)
        for i in range(len(result)):
            if random.random() < MUTATION_RATE:
                result[i] = '1' if result[i] == '0' else '0'
        return ''.join(result)

    def select(population, fitnesses):
        """錦標賽選擇"""
        tournament_size = 5
        selected = random.sample(list(zip(population, fitnesses)), tournament_size)
        return max(selected, key=lambda x: x[1])[0]

    # 初始化族群
    population = [create_chromosome() for _ in range(POPULATION_SIZE)]

    print("\n--- 演化過程 ---")
    best_solution = None
    best_fitness = 0

    for generation in range(GENERATIONS):
        # 評估適應度
        decoded = [decode(c) for c in population]
        fitnesses = [fitness(x) for x in decoded]

        # 記錄最佳解
        max_fitness = max(fitnesses)
        max_idx = fitnesses.index(max_fitness)
        if max_fitness > best_fitness:
            best_fitness = max_fitness
            best_solution = decoded[max_idx]

        if generation % 20 == 0:
            print(f"第 {generation:3d} 代: 最佳適應度 = {best_fitness:.4f}, x = {best_solution:.2f}")

        # 產生下一代
        new_population = []
        while len(new_population) < POPULATION_SIZE:
            parent1 = select(population, fitnesses)
            parent2 = select(population, fitnesses)
            child1, child2 = crossover(parent1, parent2)
            new_population.append(mutate(child1))
            if len(new_population) < POPULATION_SIZE:
                new_population.append(mutate(child2))

        population = new_population

    print(f"\n--- 最終結果 ---")
    print(f"最佳解：x = {best_solution:.4f}")
    print(f"最佳適應度：{best_fitness:.4f}")
    print(f"理論最佳：x ≈ 15.7, f(x) ≈ 15.6")

    print("\n" + "=" * 50)

if __name__ == "__main__":
    random.seed(42)
    demo()