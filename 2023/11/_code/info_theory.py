#!/usr/bin/env python3
"""資訊理論與編碼 — 示範實作"""

import math
from collections import Counter
from heapq import heapify, heappush, heappop
from functools import reduce

# ── 1. 熵與自資訊 ──────────────────────────────────

def entropy(probs):
    return -sum(p * math.log2(p) for p in probs if p > 0)

def self_info(p):
    return -math.log2(p)

# ── 2. Huffman 編碼 ────────────────────────────────

def huffman(symbols_with_probs):
    heap = [[w, [sym, ""]] for sym, w in symbols_with_probs]
    heapify(heap)
    while len(heap) > 1:
        lo = heappop(heap)
        hi = heappop(heap)
        for pair in lo[1:]:
            pair[1] = "0" + pair[1]
        for pair in hi[1:]:
            pair[1] = "1" + pair[1]
        heappush(heap, [lo[0] + hi[0]] + lo[1:] + hi[1:])
    return sorted(heappop(heap)[1:], key=lambda p: len(p[1]))

def huffman_encode(text):
    freq = Counter(text)
    total = len(text)
    probs = [(ch, cnt / total) for ch, cnt in freq.most_common()]
    codes = huffman(probs)
    code_map = {ch: code for ch, code in codes}
    encoded = "".join(code_map[ch] for ch in text)
    return encoded, code_map

# ── 3. 通道容量（BSC）─────────────────────────────

def bsc_capacity(p):
    if p == 0 or p == 1:
        return 1.0
    h = -p * math.log2(p) - (1 - p) * math.log2(1 - p)
    return 1.0 - h

# ── 4. 漢明碼 (7,4) ──────────────────────────────

def hamming_encode(bits4):
    d = list(bits4)
    p1 = d[0] ^ d[1] ^ d[3]
    p2 = d[0] ^ d[2] ^ d[3]
    p3 = d[1] ^ d[2] ^ d[3]
    return [p1, p2, d[0], p3, d[1], d[2], d[3]]

def hamming_decode(bits7):
    s1 = bits7[0] ^ bits7[2] ^ bits7[4] ^ bits7[6]
    s2 = bits7[1] ^ bits7[2] ^ bits7[5] ^ bits7[6]
    s3 = bits7[3] ^ bits7[4] ^ bits7[5] ^ bits7[6]
    err_pos = s1 * 1 + s2 * 2 + s3 * 4
    fixed = list(bits7)
    if 1 <= err_pos <= 7:
        fixed[err_pos - 1] ^= 1
    return [fixed[2], fixed[4], fixed[5], fixed[6]]

# ── demo() ─────────────────────────────────────────

def demo():
    print("=" * 60)
    print("資訊理論與編碼 — 示範")
    print("=" * 60)

    # 1. Entropy
    print("\n[1] 熵的計算")
    probs = [0.5, 0.25, 0.125, 0.125]
    H = entropy(probs)
    print(f"  機率分布: {probs}")
    print(f"  熵 H = {H:.4f} bits")
    for i, p in enumerate(probs):
        print(f"    符號 {i}: 自資訊 = {self_info(p):.4f} bits")

    # 2. Huffman
    print("\n[2] Huffman 編碼")
    text = "ABBCCCDDDDEEEEE"
    encoded, code_map = huffman_encode(text)
    print(f"  原文: {text}")
    print(f"  編碼表: {code_map}")
    print(f"  編碼後: {encoded}")
    original_bits = len(text) * 8
    encoded_bits = len(encoded)
    print(f"  原始: {original_bits} bits → 編碼後: {encoded_bits} bits")
    print(f"  壓縮比: {encoded_bits / original_bits:.2%}")

    # 3. Channel capacity
    print("\n[3] BSC 通道容量")
    for p in [0.0, 0.1, 0.25, 0.5]:
        C = bsc_capacity(p)
        print(f"  錯誤率 p={p:.2f}, 容量 C={C:.4f} bits/use")

    # 4. Hamming code
    print("\n[4] 漢明碼 (7,4)")
    test_bits = [1, 0, 1, 1]
    encoded_bits = hamming_encode(test_bits)
    print(f"  原始: {test_bits}")
    print(f"  編碼: {encoded_bits}")
    received = list(encoded_bits)
    received[3] ^= 1
    print(f"  接收(第4位錯誤): {received}")
    decoded = hamming_decode(received)
    print(f"  解碼(糾錯後): {decoded}")
    print(f"  正確: {test_bits == decoded}")

    print("\n" + "=" * 60)
    print("示範完成")
    print("=" * 60)

if __name__ == "__main__":
    demo()
