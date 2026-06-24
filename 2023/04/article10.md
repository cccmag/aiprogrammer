# 旅行推銷員問題 TSP

## 什麼是 TSP？

旅行推銷員問題（Travelling Salesman Problem, TSP）是經典的 NP-hard 問題：給定 n 個城市和城市之間的距離，找到一條經過每個城市恰好一次並返回起點的最短路徑。

TSP 的歷史可追溯到 19 世紀，但直到 1972 年 Richard Karp 證明它是 NP-complete 後，才真正成為理論電腦科學的重點研究對象。

## NP-hard 的意義

### 為什麼 TSP 很難？

對於 n 個城市，需要考慮所有排列：總共有 (n-1)!/2 條不同的路徑。當 n=10 時約 18 萬條，n=15 時約 430 億條，n=20 時約 6×10¹⁶ 條——暴力搜尋完全不可行。

### P ≠ NP 的假設

多數研究者認為 P ≠ NP，這意味著 TSP 不存在多項式時間的精確演算法。因此，我們轉而尋求近似解。

## 近似演算法

### 最近鄰居法（Nearest Neighbor）

最簡單的貪婪策略：從某個城市出發，每次都去最近且未訪問的城市。

```python
def nearest_neighbor(dist, start=0):
    n = len(dist)
    visited = [False] * n
    path = [start]
    visited[start] = True
    current = start
    for _ in range(n - 1):
        next_city = min(
            (i for i in range(n) if not visited[i]),
            key=lambda i: dist[current][i]
        )
        visited[next_city] = True
        path.append(next_city)
        current = next_city
    path.append(start)
    return path
```

時間複雜度 O(n²)，但解的品質不保證——最壞情況可能比最優解差很多。

### 最小生成樹法（MST-based）

基於 MST 的 2-近似演算法：
1. 計算最小生成樹（MST）
2. 對 MST 進行 DFS 得到一條路徑
3. 跳過重複訪問的頂點

這保證總路徑長度不超過最優解的兩倍。

### Christofides 演算法

改進的 3/2-近似演算法：
1. 計算 MST
2. 找出 MST 中度數為奇數的頂點，計算最小權重完美匹配
3. 合併 MST 和匹配，形成尤拉圖
4. 走尤拉迴路並跳過重複頂點

```python
def christofides(dist):
    n = len(dist)
    # 1. 計算 MST（例如 Prim）
    mst = prim_mst(dist)
    # 2. 找奇數度頂點
    odd_vertices = [i for i in range(n)
                    if len(mst[i]) % 2 == 1]
    # 3. 最小權重完美匹配
    matching = min_weight_matching(dist, odd_vertices)
    # 4. 合併形成尤拉圖
    eulerian_graph = merge(mst, matching)
    # 5. 找尤拉迴路並短路
    euler_tour = find_euler_tour(eulerian_graph)
    hamiltonian = shortcut(euler_tour)
    return hamiltonian
```

這是目前最好的多項式時間近似演算法，保證 1.5 倍的近似比。

## 啟發式演算法

### 模擬退火（Simulated Annealing）

```python
import random, math

def simulated_annealing(dist, temp_start=1000,
                        temp_end=0.01, cooling_rate=0.995):
    n = len(dist)
    path = list(range(n))
    random.shuffle(path)
    path.append(path[0])
    current_cost = path_cost(path, dist)
    best_path, best_cost = path[:], current_cost
    temp = temp_start
    while temp > temp_end:
        i, j = random.sample(range(1, n), 2)
        new_path = path[:]
        new_path[i], new_path[j] = new_path[j], new_path[i]
        new_cost = path_cost(new_path, dist)
        delta = new_cost - current_cost
        if delta < 0 or random.random() < math.exp(-delta/temp):
            path, current_cost = new_path, new_cost
            if current_cost < best_cost:
                best_path, best_cost = path[:], current_cost
        temp *= cooling_rate
    return best_path, best_cost
```

### 遺傳演算法（Genetic Algorithm）

模擬自然選擇：將路徑視為染色體，透過交配（merge 兩個路徑）和變異（交換兩個城市）產生後代。

### 蟻群演算法（Ant Colony）

模擬螞蟻覓食行為：螞蟻在走過的路徑上留下費洛蒙，後續螞蟻傾向於選擇費洛蒙濃度高的路徑。

## 實際應用

TSP 的應用遠超旅遊規劃：

- **電路設計**：鑽孔機的路徑規劃（減少移動距離）
- **物流配送**：車輛路徑問題（Vehicle Routing Problem）
- **基因組學**：DNA 定序（片段重組）
- **生產排程**：機器人組裝順序
- **天文觀測**：望遠鏡觀測目標排序

## TSP 在現代 AI 中

近年來，深度學習也被應用於 TSP：
- **Pointer Networks**：基於注意力機制直接輸出路徑
- **Reinforcement Learning**：將 TSP 視為馬可夫決策過程
- **Graph Neural Networks**：在圖結構上學習路徑表示

但對於大規模 TSP，傳統的啟發式演算法（如 LKH）仍然是最強的。

## 總結

TSP 是 NP-hard 問題中最著名的一個。它教會我們：當遇到本質上困難的問題時，不要追求完美，而是尋找「足夠好」的解決方案。近似演算法和啟發式演算法為這類問題提供了實用的出路。

## 延伸閱讀

- [TSP Approximation Algorithms](https://www.google.com/search?q=TSP+approximation+algorithm)
- [Christofides Algorithm](https://www.google.com/search?q=Christofides+algorithm)
- [Ant Colony Optimization](https://www.google.com/search?q=ant+colony+optimization+TSP)
