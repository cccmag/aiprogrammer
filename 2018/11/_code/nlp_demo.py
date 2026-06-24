import numpy as np
import math


def softmax(x):
    exp_x = np.exp(x - np.max(x, axis=-1, keepdims=True))
    return exp_x / (np.sum(exp_x, axis=-1, keepdims=True) + 1e-10)


def cosine_similarity(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b) + 1e-10)


def demo():
    print("=" * 56)
    print("NLP 概念示範")
    print("=" * 56)

    print("\n[1] 詞嵌入與相似度")
    vocab = {
        "機器學習": 0, "深度學習": 1, "人工智慧": 2, "蘋果": 3,
        "香蕉": 4, "水果": 5, "狗": 6, "貓": 7, "動物": 8, "汽車": 9
    }

    embedding = np.random.randn(10, 64) * 0.1
    print(f"詞向量維度: {embedding.shape[1]}")
    print(f"詞彙表大小: {len(vocab)}")

    ml_sim = cosine_similarity(embedding[0], embedding[1])
    apple_ml_sim = cosine_similarity(embedding[3], embedding[0])
    print(f"「機器學習」與「深度學習」相似度: {ml_sim:.2f}")
    print(f"「機器學習」與「蘋果」相似度: {apple_ml_sim:.2f}")

    print("\n[2] Self-Attention")
    seq_len = 3
    d_model = 64
    num_heads = 4
    d_k = d_model // num_heads

    x = np.random.randn(1, seq_len, d_model)

    W_q = np.random.randn(d_model, d_model) * 0.02
    W_k = np.random.randn(d_model, d_model) * 0.02
    W_v = np.random.randn(d_model, d_model) * 0.02

    Q = np.tensordot(x, W_q, axes=1)
    K = np.tensordot(x, W_k, axes=1)
    V = np.tensordot(x, W_v, axes=1)

    Q = Q.reshape(1, seq_len, num_heads, d_k).transpose(0, 2, 1, 3)
    K = K.reshape(1, seq_len, num_heads, d_k).transpose(0, 2, 1, 3)
    V = V.reshape(1, seq_len, num_heads, d_k).transpose(0, 2, 1, 3)

    print(f"查詢向量維度: {Q.shape}")
    print(f"鍵向量維度: {K.shape}")

    scores = np.matmul(Q, K.transpose(0, 1, 3, 2)) / math.sqrt(d_k)
    attention_weights = softmax(scores)
    print(f"注意力權重形狀: {attention_weights.shape}")

    attn_output = np.matmul(attention_weights, V)
    print(f"注意力輸出維度: {attn_output.shape}")

    print("\n[3] 位置編碼")
    max_seq_len = 10
    pe = np.zeros((max_seq_len, d_model))
    for pos in range(max_seq_len):
        for i in range(0, d_model, 2):
            pe[pos, i] = math.sin(pos / (10000 ** (i / d_model)))
            if i + 1 < d_model:
                pe[pos, i + 1] = math.cos(pos / (10000 ** (i / d_model)))
    print(f"位置編碼形狀: {pe.shape}")
    print(f"位置編碼範圍: [{pe.min():.4f}, {pe.max():.4f}]")

    print("\n[4] 序列編碼")
    x_with_pe = x + pe[:seq_len, :d_model]
    print(f"輸入（含位置編碼）形狀: {x_with_pe.shape}")
    output = np.tanh(np.matmul(attention_weights, V).transpose(0, 2, 1, 3).reshape(1, seq_len, d_model))
    print(f"最終輸出維度: {output.shape}")

    print(f"\n{'=' * 56}")
    print("示範完成")
    print("=" * 56)


if __name__ == "__main__":
    demo()