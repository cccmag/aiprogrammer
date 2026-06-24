import numpy as np
import math


def softmax(x):
    exp_x = np.exp(x - np.max(x, axis=-1, keepdims=True))
    return exp_x / np.sum(exp_x, axis=-1, keepdims=True)


def get_positional_encoding(max_seq_len, d_model):
    pe = np.zeros((max_seq_len, d_model))
    for pos in range(max_seq_len):
        for i in range(0, d_model, 2):
            pe[pos, i] = math.sin(pos / (10000 ** (i / d_model)))
            if i + 1 < d_model:
                pe[pos, i + 1] = math.cos(pos / (10000 ** (i / d_model)))
    return pe


def demo():
    print("=" * 56)
    print("BERT 概念示範")
    print("=" * 56)

    d_model = 768
    max_seq_len = 10

    print(f"\n[1] 輸入文本")
    text = "[CLS] BERT 是強大的語言模型 [SEP]"
    print(f"原始文字: \"{text}\"")

    vocab = {
        "[CLS]": 101, "[SEP]": 102, "[MASK]": 103,
        "BERT": 2361, "是": 3221, "強": 5283, "大": 1920,
        "的": 4633, "語": 6427, "言": 6241, "模": 3563, "型": 1814
    }

    tokens = text.split()
    token_ids = [vocab.get(t, 100) for t in tokens]
    print(f"詞索引: {token_ids}")
    print(f"詞嵌入維度: {d_model}")

    print(f"\n[2] 位置編碼")
    pe = get_positional_encoding(max_seq_len, 64)
    print(f"位置編碼形狀: {pe.shape}")
    print(f"位置編碼範圍: [{pe.min():.4f}, {pe.max():.4f}]")

    print(f"\n[3] Transformer 層輸出")
    batch_size = 1
    seq_len = len(tokens)
    hidden = np.random.randn(seq_len, 64) * 0.02

    num_heads = 4
    d_k = 64 // num_heads

    Q = hidden @ np.random.randn(64, 64) * 0.02
    K = hidden @ np.random.randn(64, 64) * 0.02
    V = hidden @ np.random.randn(64, 64) * 0.02

    Q = Q.reshape(batch_size, seq_len, num_heads, d_k).transpose(0, 2, 1, 3)
    K = K.reshape(batch_size, seq_len, num_heads, d_k).transpose(0, 2, 1, 3)
    V = V.reshape(batch_size, seq_len, num_heads, d_k).transpose(0, 2, 1, 3)

    scores = np.matmul(Q, K.transpose(0, 1, 3, 2)) / math.sqrt(d_k)
    attention_weights = softmax(scores)
    attn_output = np.matmul(attention_weights, V)
    attn_output = attn_output.transpose(0, 2, 1, 3).reshape(batch_size, seq_len, 64)

    print(f"注意力權重形狀: {attention_weights.shape}")
    print(f"輸出形狀: {attn_output.shape}")

    print(f"\n[4] MLM 預訓練")
    masked_indices = [1, 2]
    print(f"遮蓋位置: {masked_indices}")
    vocab_size = 30000
    print(f"預測機率分佈形狀: ({len(masked_indices)}, {vocab_size})")
    loss = np.random.random()
    print(f"損失值: {loss:.4f}")

    print(f"\n{'=' * 56}")
    print("示範完成")
    print("=" * 56)


if __name__ == "__main__":
    demo()