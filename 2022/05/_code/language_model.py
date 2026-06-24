import numpy as np
from collections import Counter
import math
import random

class CBOW:
    def __init__(self, vocab_size, embed_dim):
        self.W = np.random.randn(vocab_size, embed_dim) * 0.01
        self.W2 = np.random.randn(embed_dim, vocab_size) * 0.01

    def forward(self, context_indices):
        h = np.mean(self.W[context_indices], axis=0)
        u = h @ self.W2
        exp_u = np.exp(u - np.max(u))
        probs = exp_u / np.sum(exp_u)
        return h, probs

    def train(self, contexts, targets, lr=0.01):
        loss = 0
        for ctx, tgt in zip(contexts, targets):
            h, probs = self.forward(ctx)
            loss -= math.log(probs[tgt] + 1e-10)
            grad = probs.copy()
            grad[tgt] -= 1
            self.W2 -= lr * np.outer(h, grad)
            self.W[ctx] -= lr * (grad @ self.W2.T) / len(ctx)
        return loss


class RNNLM:
    def __init__(self, vocab_size, hidden_dim):
        self.Wxh = np.random.randn(hidden_dim, vocab_size) * 0.01
        self.Whh = np.random.randn(hidden_dim, hidden_dim) * 0.01
        self.Why = np.random.randn(vocab_size, hidden_dim) * 0.01
        self.bh = np.zeros((hidden_dim, 1))
        self.by = np.zeros((vocab_size, 1))

    def forward(self, inputs, hprev):
        xs, hs, ys, ps = {}, {}, {}, {}
        hs[-1] = np.copy(hprev)
        for t in range(len(inputs)):
            xs[t] = np.zeros((self.Wxh.shape[1], 1))
            xs[t][inputs[t]] = 1
            hs[t] = np.tanh(self.Wxh @ xs[t] + self.Whh @ hs[t-1] + self.bh)
            ys[t] = self.Why @ hs[t] + self.by
            ps[t] = np.exp(ys[t] - np.max(ys[t]))
            ps[t] /= np.sum(ps[t])
        return hs, ps

    def loss(self, inputs, targets):
        hs, ps = self.forward(inputs, np.zeros((self.Whh.shape[0], 1)))
        loss = 0
        for t in range(len(inputs)):
            loss -= math.log(ps[t][targets[t], 0] + 1e-10)
        return loss

    def train(self, inputs, targets, lr=0.1):
        xs = {}
        hs, ps = self.forward(inputs, np.zeros((self.Whh.shape[0], 1)))
        for t in range(len(inputs)):
            xs[t] = np.zeros((self.Wxh.shape[1], 1))
            xs[t][inputs[t]] = 1
        dWxh = np.zeros_like(self.Wxh)
        dWhh = np.zeros_like(self.Whh)
        dWhy = np.zeros_like(self.Why)
        dbh = np.zeros_like(self.bh)
        dby = np.zeros_like(self.by)
        dhnext = np.zeros_like(hs[0])
        loss = 0
        for t in reversed(range(len(inputs))):
            dy = np.copy(ps[t])
            dy[targets[t]] -= 1
            dWhy += dy @ hs[t].T
            dby += dy
            dh = self.Why.T @ dy + dhnext
            dtanh = (1 - hs[t] * hs[t]) * dh
            dbh += dtanh
            dWxh += dtanh @ xs[t].T
            dWhh += dtanh @ (hs[t-1].T if t > 0 else np.zeros((1, self.Whh.shape[1])))
            dhnext = self.Whh.T @ dtanh
            loss -= math.log(ps[t][targets[t], 0] + 1e-10)
        for param, dparam in zip([self.Wxh, self.Whh, self.Why, self.bh, self.by],
                                 [dWxh, dWhh, dWhy, dbh, dby]):
            param -= lr * dparam
        return loss


def beam_search(model, start_idx, vocab_size, beam_width=3, max_len=10):
    sequences = [[[start_idx], 0.0]]
    for _ in range(max_len):
        all_candidates = []
        for seq, score in sequences:
            if seq[-1] == 0:
                all_candidates.append((seq, score))
                continue
            hs, ps = model.forward([seq[-1]], np.zeros((model.Whh.shape[0], 1)))
            probs = ps[0].flatten()
            for i in range(vocab_size):
                candidate = seq + [i]
                all_candidates.append((candidate, score - math.log(probs[i] + 1e-10)))
        sequences = sorted(all_candidates, key=lambda x: x[1])[:beam_width]
    return sequences


def perplexity(model, corpus_indices, seq_len=5):
    total_loss = 0
    total_tokens = 0
    for i in range(0, len(corpus_indices) - seq_len):
        inputs = corpus_indices[i:i+seq_len]
        targets = corpus_indices[i+1:i+seq_len+1]
        total_loss += model.loss(inputs, targets)
        total_tokens += seq_len
    return math.exp(total_loss / total_tokens)


def demo():
    print("=== Language Model Demo ===")
    corpus = "the cat sat on the mat the dog sat on the log the bird sat on the tree"
    words = corpus.split()
    vocab = list(set(words))
    w2i = {w: i for i, w in enumerate(vocab)}
    i2w = {i: w for w, i in w2i.items()}
    data = [w2i[w] for w in words]

    print("\n--- CBOW Word2Vec ---")
    cbow = CBOW(len(vocab), 10)
    contexts, targets = [], []
    for i in range(2, len(data)-2):
        contexts.append(data[i-2:i] + data[i+1:i+3])
        targets.append(data[i])
    for epoch in range(100):
        loss = cbow.train(contexts, targets, lr=0.05)
        if epoch % 20 == 0:
            print(f"Epoch {epoch}: loss={loss:.4f}")

    print("\n--- RNN Language Model ---")
    rnn = RNNLM(len(vocab), 20)
    for epoch in range(100):
        loss = rnn.train(data[:-1], data[1:], lr=0.01)
        if epoch % 20 == 0:
            print(f"Epoch {epoch}: loss={loss:.4f}")

    ppl = perplexity(rnn, data, seq_len=3)
    print(f"\nPerplexity on corpus: {ppl:.4f}")

    print("\n--- Beam Search Generation ---")
    beams = beam_search(rnn, data[0], len(vocab), beam_width=3, max_len=6)
    for seq, score in beams[:3]:
        gen_words = [i2w.get(i, "?") for i in seq]
        print(f"Score={score:.4f}: {' '.join(gen_words)}")

    print("\nDemo complete!")


if __name__ == "__main__":
    demo()
