#!/usr/bin/env python3
"""Attention Mechanisms: Bahdanau, Luong, Self-Attention, Visualization"""

import numpy as np

def softmax(x, axis=-1):
    e = np.exp(x - np.max(x, axis=axis, keepdims=True))
    return e / np.sum(e, axis=axis, keepdims=True)

def bahdanau_score(query, keys, W_q, W_k, v):
    query_trans = W_q @ query
    keys_trans = W_k @ keys.T
    energies = v @ np.tanh(query_trans[:, None] + keys_trans)
    return energies

def bahdanau_attention(query, keys, values, W_q, W_k, v):
    scores = bahdanau_score(query, keys, W_q, W_k, v)
    weights = softmax(scores)
    context = weights @ values
    return context, weights

def luong_score(query, keys, method="dot"):
    if method == "dot":
        return query @ keys.T
    elif method == "general":
        W = np.random.randn(len(query), len(query)) * 0.1
        return (W @ query) @ keys.T
    elif method == "concat":
        W = np.random.randn(len(query), len(query)) * 0.1
        v = np.random.randn(len(query)) * 0.1
        return v @ np.tanh(W @ (query[:, None] + keys))
    raise ValueError(f"Unknown method: {method}")

def luong_attention(query, keys, values, method="dot"):
    scores = luong_score(query, keys, method)
    weights = softmax(scores)
    context = weights @ values
    return context, weights

def self_attention(Q, K, V, mask=None):
    d_k = K.shape[-1]
    scores = Q @ K.T / np.sqrt(d_k)
    if mask is not None:
        scores = np.where(mask, -1e9, scores)
    weights = softmax(scores, axis=-1)
    output = weights @ V
    return output, weights

def multi_head_attention(Q, K, V, num_heads=4):
    d_model = Q.shape[-1]
    d_k = d_model // num_heads
    W_q = np.random.randn(num_heads, d_model, d_k) * 0.1
    W_k = np.random.randn(num_heads, d_model, d_k) * 0.1
    W_v = np.random.randn(num_heads, d_model, d_k) * 0.1
    W_o = np.random.randn(num_heads * d_k, d_model) * 0.1

    heads = []
    for h in range(num_heads):
        q = Q @ W_q[h]; k = K @ W_k[h]; v = V @ W_v[h]
        scores = q @ k.T / np.sqrt(d_k)
        weights = softmax(scores, axis=-1)
        head_out = weights @ v
        heads.append(head_out)

    concat = np.concatenate(heads, axis=-1)
    output = concat @ W_o
    return output

def visualize_attention(weights, tokens, title="Attention Weights"):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    fig, ax = plt.subplots(figsize=(8, 6))
    im = ax.imshow(weights, cmap="Blues", aspect="auto")
    ax.set_xticks(range(len(tokens)))
    ax.set_yticks(range(len(tokens)))
    ax.set_xticklabels(tokens, rotation=45, ha="right")
    ax.set_yticklabels(tokens)
    ax.set_title(title)
    fig.colorbar(im, ax=ax)
    fig.tight_layout()
    fig.savefig("attention_vis.png", dpi=100)
    plt.close(fig)
    print(f"[viz] Saved {title} -> attention_vis.png")

def demo():
    np.random.seed(42)
    print("=" * 60)
    print("Attention Mechanisms Demo")
    print("=" * 60)

    tokens = ["我", "愛", "程", "式", "設", "計"]
    n = len(tokens)
    d = 8

    query = np.random.randn(d)
    keys = np.random.randn(n, d)
    values = np.random.randn(n, d)

    W_q = np.random.randn(d, d) * 0.1
    W_k = np.random.randn(d, d) * 0.1
    v = np.random.randn(d) * 0.1

    ctx_b, w_b = bahdanau_attention(query, keys, values, W_q, W_k, v)
    print("\n[Bahdanau Attention]")
    print(f"  context shape: {ctx_b.shape}")
    print(f"  weights: {np.round(w_b, 3)}")

    ctx_l, w_l = luong_attention(query, keys, values, "dot")
    print("\n[Luong Attention (dot)]")
    print(f"  context shape: {ctx_l.shape}")
    print(f"  weights: {np.round(w_l, 3)}")

    Q = np.random.randn(n, d)
    K = np.random.randn(n, d)
    V = np.random.randn(n, d)

    out_sa, w_sa = self_attention(Q, K, V)
    print("\n[Self-Attention]")
    print(f"  output shape: {out_sa.shape}")
    print(f"  weights shape: {w_sa.shape}")
    np.set_printoptions(precision=3, suppress=True)
    print(f"  weights:\n{w_sa}")

    out_mh = multi_head_attention(Q, K, V, num_heads=4)
    print(f"\n[Multi-Head Attention]")
    print(f"  output shape: {out_mh.shape}")

    causal_mask = np.triu(np.ones((n, n)), k=1).astype(bool)
    out_causal, w_causal = self_attention(Q, K, V, mask=causal_mask)
    print(f"\n[Causal Self-Attention]")
    print(f"  masked weights:\n{w_causal}")

    try:
        visualize_attention(w_sa, tokens, "Self-Attention Weights")
    except Exception as e:
        print(f"[viz] skipped ({e})")

    print("\n" + "=" * 60)
    print("Demo complete!")
    print("=" * 60)

if __name__ == "__main__":
    demo()
