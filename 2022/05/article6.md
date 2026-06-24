# Beam Search 解碼

## 解碼策略概覽

語言模型在生成文本時，需要從機率分布中選擇詞。不同的解碼策略會產生截然不同的結果。

## 貪婪解碼

最簡單的策略：每一步只選機率最高的詞：

```python
def greedy_decode(model, start, max_len=30):
    result = [start]
    for _ in range(max_len):
        probs = model.predict(result)
        next_word = argmax(probs[-1])
        if next_word == EOS:
            break
        result.append(next_word)
    return result
```

**問題**：貪婪解碼是短視的——當下最好的選擇可能導致後續不佳。

## Beam Search

Beam Search 在每一步保留 k 個候選序列：

```python
def beam_search_decode(model, start, beam_width=3, max_len=30):
    # 每個候選：([sequence], log_prob)
    candidates = [([start], 0.0)]

    for step in range(max_len):
        all_candidates = []

        for seq, score in candidates:
            if seq[-1] == EOS:
                all_candidates.append((seq, score))
                continue

            probs = model.predict(seq)
            log_probs = log(probs[-1])

            for i, log_p in enumerate(log_probs):
                new_seq = seq + [i]
                new_score = score - log_p  # 負對數機率
                all_candidates.append((new_seq, new_score))

        # 保留分數最低（機率最高）的 k 個
        candidates = sorted(all_candidates, key=lambda x: x[1])[:beam_width]

    return candidates[0][0]
```

### 長度正規化

Beam Search 傾向於選擇較短的序列（因為機率是乘積，越長越小）。解決方案是加入長度正規化：

```python
def length_normalized_score(seq, log_prob, alpha=0.75):
    return log_prob / (len(seq) ** alpha)
```

## Top-k 採樣

只從機率最高的 k 個詞中採樣：

```python
def top_k_sampling(probs, k=10):
    # 保留前 k 個最高機率
    top_k_probs, top_k_indices = torch.topk(probs, k)
    # 重新歸一化
    top_k_probs = F.softmax(top_k_probs, dim=0)
    # 從中採樣
    return top_k_indices[torch.multinomial(top_k_probs, 1)]
```

## Top-p（Nucleus）採樣

從累積機率達到 p 的最小詞集合中採樣：

```python
def top_p_sampling(probs, p=0.9):
    sorted_probs, sorted_indices = torch.sort(probs, descending=True)
    cumulative = torch.cumsum(sorted_probs, dim=0)
    # 找出累積機率超過 p 的位置
    cutoff = torch.searchsorted(cumulative, p) + 1
    # 保留前 cutoff 個詞
    nucleus_probs = sorted_probs[:cutoff]
    nucleus_probs = nucleus_probs / nucleus_probs.sum()
    chosen = torch.multinomial(nucleus_probs, 1)
    return sorted_indices[chosen]
```

## 解碼策略對比

| 策略 | 多樣性 | 連貫性 | 可控性 |
|------|--------|--------|--------|
| Greedy | 低 | 中 | 低 |
| Beam Search | 低 | 高 | 中 |
| Top-k | 中 | 中 | 高 |
| Top-p | 高 | 高 | 高 |
| Temperature | 可調 | 可調 | 高 |

## 建議

- **機器翻譯**：Beam Search（beam width 4-10）
- **故事生成**：Top-p（p=0.9）+ 溫度 0.8
- **程式碼生成**：Beam Search + Top-k 混合
- **對話系統**：Top-p（p=0.9-0.95）

## 延伸閱讀

- [Beam Search 詳解](https://www.google.com/search?q=beam+search+decoding+explained)
- [The Curious Case of Neural Text Generation](https://www.google.com/search?q=curious+case+of+neural+text+generation)
- [Top-p Sampling 論文](https://www.google.com/search?q=nucleus+sampling+top+p+decoding)
