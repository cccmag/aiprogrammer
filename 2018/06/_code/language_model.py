#!/usr/bin/env python3
"""簡單的 N-gram 語言模型"""

import random
import re
from collections import defaultdict

class NGramLM:
    def __init__(self, n):
        self.n = n
        self.ngram_counts = defaultdict(int)
        self.context_counts = defaultdict(int)
        self.vocab = set()

    def tokenize(self, text):
        return re.findall(r'\w+', text.lower())

    def train(self, corpus):
        tokens = self.tokenize(corpus)
        for i in range(len(tokens) - self.n + 1):
            ngram = tuple(tokens[i:i+self.n])
            context = ngram[:-1]
            self.ngram_counts[ngram] += 1
            self.context_counts[context] += 1
            self.vocab.update(tokens)

    def probability(self, ngram):
        context = ngram[:-1]
        count = self.ngram_counts[ngram]
        context_count = self.context_counts[context]
        return count / context_count if context_count > 0 else 1e-10

    def predict_next(self, context):
        best_word = None
        best_prob = 0
        for ngram, count in self.ngram_counts.items():
            if ngram[:-1] == context:
                prob = count / self.context_counts[context]
                if prob > best_prob:
                    best_prob = prob
                    best_word = ngram[-1]
        return best_word, best_prob

    def generate(self, seed, max_words=20):
        words = self.tokenize(seed)
        if len(words) < self.n - 1:
            words.extend(['<s>'] * (self.n - 1 - len(words)))

        for _ in range(max_words):
            context = tuple(words[-(self.n-1):])
            if len(context) < self.n - 1:
                context = tuple(['<s>'] * (self.n - 1 - len(context)) + list(context))

            next_word, _ = self.predict_next(context)
            if next_word is None:
                break
            words.append(next_word)

        return ' '.join(words[self.n-1:])

def demo():
    print('=' * 50)
    print('語言模型：N-gram 文字生成')
    print('=' * 50)
    print()

    corpus = """
    the quick brown fox jumps over the lazy dog
    a quick brown dog jumps over the lazy fox
    the lazy dog sleeps in the sun
    a quick fox jumps over the lazy dog
    the brown fox is very quick
    a lazy dog is a happy dog
    """

    model = NGramLM(n=3)
    model.train(corpus)

    seeds = ['the quick', 'a lazy', 'a quick fox']
    for seed in seeds:
        generated = model.generate(seed, max_words=10)
        print(f'  輸入: "{seed}"')
        print(f'  生成: "{generated}"')
        print()

if __name__ == '__main__':
    demo()