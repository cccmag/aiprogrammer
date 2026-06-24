#!/usr/bin/env python3
"""Algorithm Design & Analysis - Demo"""

def merge_sort(arr):
    if len(arr) <= 1:
        return arr
    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])
    return merge(left, right)

def merge(left, right):
    result = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    result.extend(left[i:])
    result.extend(right[j:])
    return result

def lcs(X, Y):
    m, n = len(X), len(Y)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if X[i - 1] == Y[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1
            else:
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])
    i, j = m, n
    seq = []
    while i > 0 and j > 0:
        if X[i - 1] == Y[j - 1]:
            seq.append(X[i - 1])
            i -= 1
            j -= 1
        elif dp[i - 1][j] >= dp[i][j - 1]:
            i -= 1
        else:
            j -= 1
    return dp[m][n], ''.join(reversed(seq))

def knapSack(W, wt, val, n):
    dp = [[0] * (W + 1) for _ in range(n + 1)]
    for i in range(1, n + 1):
        for w in range(1, W + 1):
            if wt[i - 1] <= w:
                dp[i][w] = max(val[i - 1] + dp[i - 1][w - wt[i - 1]], dp[i - 1][w])
            else:
                dp[i][w] = dp[i - 1][w]
    w = W
    items = []
    for i in range(n, 0, -1):
        if dp[i][w] != dp[i - 1][w]:
            items.append(i - 1)
            w -= wt[i - 1]
    return dp[n][W], list(reversed(items))

import heapq
from collections import Counter

class HuffmanNode:
    def __init__(self, char, freq):
        self.char = char
        self.freq = freq
        self.left = None
        self.right = None
    def __lt__(self, other):
        return self.freq < other.freq

def huffman_encoding(text):
    freq = Counter(text)
    heap = [HuffmanNode(c, f) for c, f in freq.items()]
    heapq.heapify(heap)
    while len(heap) > 1:
        left = heapq.heappop(heap)
        right = heapq.heappop(heap)
        merged = HuffmanNode(None, left.freq + right.freq)
        merged.left = left
        merged.right = right
        heapq.heappush(heap, merged)
    root = heap[0]
    codes = {}
    def dfs(node, code):
        if node.char is not None:
            codes[node.char] = code
            return
        if node.left:
            dfs(node.left, code + '0')
        if node.right:
            dfs(node.right, code + '1')
    dfs(root, '')
    encoded = ''.join(codes[c] for c in text)
    return encoded, codes

def ford_fulkerson(graph, source, sink):
    n = len(graph)
    flow = [[0] * n for _ in range(n)]
    parent = [-1] * n

    def bfs():
        visited = [False] * n
        queue = [source]
        visited[source] = True
        while queue:
            u = queue.pop(0)
            for v in range(n):
                if not visited[v] and graph[u][v] - flow[u][v] > 0:
                    visited[v] = True
                    parent[v] = u
                    if v == sink:
                        return True
                    queue.append(v)
        return visited[sink]

    max_flow = 0
    while bfs():
        path_flow = float('inf')
        v = sink
        while v != source:
            u = parent[v]
            path_flow = min(path_flow, graph[u][v] - flow[u][v])
            v = u
        v = sink
        while v != source:
            u = parent[v]
            flow[u][v] += path_flow
            flow[v][u] -= path_flow
            v = u
        max_flow += path_flow
    return max_flow

def demo():
    print("=== Algorithm Design & Analysis Demo ===\n")

    print("1. Merge Sort")
    data = [38, 27, 43, 3, 9, 82, 10]
    print(f"Input: {data}")
    sorted_data = merge_sort(data)
    print(f"Output: {sorted_data}\n")

    print("2. Longest Common Subsequence (LCS)")
    X = "ABCBDAB"
    Y = "BDCABC"
    length, seq = lcs(X, Y)
    print(f"X={X}, Y={Y}")
    print(f"LCS Length: {length}, Sequence: {seq}\n")

    print("3. 0/1 Knapsack Problem")
    val = [60, 100, 120]
    wt = [10, 20, 30]
    W = 50
    max_val, items = knapSack(W, wt, val, len(val))
    print(f"Weights: {wt}, Values: {val}, Capacity: {W}")
    print(f"Max Value: {max_val}, Items: {items}\n")

    print("4. Huffman Coding")
    text = "A SIMPLE STRING TO BE ENCODED"
    encoded, codes = huffman_encoding(text)
    print(f"Original: {text}")
    print(f"Encoded: {encoded}")
    print(f"Codes: {codes}")
    print(f"Compression: {len(text)*8} -> {len(encoded)} bits\n")

    print("5. Ford-Fulkerson Max Flow")
    graph = [
        [0, 16, 13, 0, 0, 0],
        [0, 0, 10, 12, 0, 0],
        [0, 4, 0, 0, 14, 0],
        [0, 0, 9, 0, 0, 20],
        [0, 0, 0, 7, 0, 4],
        [0, 0, 0, 0, 0, 0]
    ]
    max_flow = ford_fulkerson(graph, 0, 5)
    print(f"Max Flow from source(0) to sink(5): {max_flow}\n")

    print("=== All demos completed ===")

if __name__ == "__main__":
    demo()
