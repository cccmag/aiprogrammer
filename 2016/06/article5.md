# 自動機理論在自然語言處理

## 前言

自然語言處理（NLP）中的許多任務都可以用自動機理論來建模和處理。有限狀態傳感器（FST）和有限狀態自動機在形態學分析、拼寫檢查、機器翻譯等領域有著廣泛應用。

## 有限狀態傳感器（FST）

### 什麼是 FST？

有限狀態傳感器（Finite-State Transducer）是一種特殊的有限自動機，可以在狀態轉換時產生輸出。

```python
class FST:
    def __init__(self, states, alphabet, transitions, initial, finals):
        self.states = states
        self.alphabet = alphabet
        self.transitions = transitions
        self.initial = initial
        self.finals = finals

    def transduce(self, input_string):
        """將輸入字串轉換為輸出"""
        state = self.initial
        output = []

        for symbol in input_string:
            if (state, symbol) in self.transitions:
                next_state, output_symbol = self.transitions[(state, symbol)]
                state = next_state
                if output_symbol:
                    output.append(output_symbol)
            else:
                return None

        if state in self.finals:
            return ''.join(output)
        return None


def fst_demo():
    # 簡單的複數形態變化
    # 規則：word -> word + 's'（大部分名詞）
    #       word -> word + 'es'（以 s, x, ch, sh 結尾）
    states = {'q0', 'q1', 'q2'}
    alphabet = {'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm',
                'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z'}

    transitions = {}
    for c in alphabet:
        if c in {'s', 'x', 'c', 'h', 's', 'h'}:
            transitions[('q0', c)] = ('q1', c)
        else:
            transitions[('q0', c)] = ('q2', c)

    transitions[('q1', '')] = ('q2', 'e')
    transitions[('q2', '')] = ('q2', 's')

    fst = FST(states, alphabet, transitions, 'q0', {'q2'})

    words = ['cat', 'dog', 'box', 'church']
    for word in words:
        result = fst.transduce(word)
        print(f"{word} -> {result}")

fst_demo()
```

## 形態學分析

### 有限狀態morphology

```python
class MorphologicalAnalyzer:
    def __init__(self):
        self.lexicon = {
            'cat': 'Noun',
            'dog': 'Noun',
            'walk': 'Verb',
            'run': 'Verb',
        }
        self.morph_rules = {
            'Noun': [
                ('', ''),      # 單數
                ('s', ''),     # 複數
            ],
            'Verb': [
                ('', 's'),     # 第三人稱單數
                ('', 'ed'),    # 過去式
                ('', 'ing'),   # 現在進行式
            ],
        }

    def analyze(self, word):
        # 嘗試各種詞素組合
        for pos, rules in self.morph_rules.items():
            for suffix, inflection in rules:
                if word.endswith(suffix):
                    stem = word[:-len(suffix)] if suffix else word
                    if stem in self.lexicon:
                        return {
                            'stem': stem,
                            'pos': pos,
                            'inflection': inflection
                        }
        return None


def morphology_demo():
    analyzer = MorphologicalAnalyzer()
    words = ['cats', 'dogs', 'walked', 'running']

    for word in words:
        result = analyzer.analyze(word)
        print(f"{word}: {result}")

morphology_demo()
```

## 正規表達式與 NLP

### 模式匹配

```python
import re

class PatternMatcher:
    def __init__(self):
        self.patterns = [
            (r'\b\d{4}-\d{2}-\d{2}\b', 'DATE'),
            (r'\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b', 'IP'),
            (r'\b[A-Z][a-z]+\b', 'PROPER_NOUN'),
            (r'\b\d+\b', 'NUMBER'),
            (r'\b\w+@\w+\.\w+\b', 'EMAIL'),
        ]
        self.compiled = [(re.compile(p), label) for p, label in self.patterns]

    def match(self, text):
        results = []
        for pattern, label in self.compiled:
            for match in pattern.finditer(text):
                results.append((match.group(), label, match.start()))
        return sorted(results, key=lambda x: x[2])


def pattern_matching_demo():
    text = "On 2026-06-15, John visited 192.168.1.1 and emailed john@example.com."

    matcher = PatternMatcher()
    results = matcher.match(text)

    for token, label, pos in results:
        print(f"{pos}: {token} ({label})")

pattern_matching_demo()
```

## 有限狀態Matcher用於斷詞

### 最小狀態Matcher（MM）

```python
class MaximumMatcher:
    def __init__(self, dictionary):
        self.dictionary = set(dictionary)

    def segment(self, text):
        """最大匹配分詞"""
        result = []
        i = 0
        while i < len(text):
            matched = text[i]
            for j in range(len(text), i, -1):
                word = text[i:j]
                if word in self.dictionary:
                    matched = word
                    break
            result.append(matched)
            i += len(matched)
        return result


class MinimumMatcher:
    def __init__(self, dictionary):
        self.dictionary = set(dictionary)

    def segment(self, text):
        """正向最小匹配分詞"""
        result = []
        i = 0
        while i < len(text):
            matched = text[i]
            for j in range(i + 1, len(text) + 1):
                word = text[i:j]
                if word in self.dictionary:
                    matched = word
            result.append(matched)
            i += len(matched)
        return result


def word_segmentation_demo():
    dictionary = ['我', '们', '我们', '是', '学生', '学习', '机器', '机器学习']

    text = "我们是学生我们学习机器学习"

    max_matcher = MaximumMatcher(dictionary)
    min_matcher = MinimumMatcher(dictionary)

    print(f"Max matching: {max_matcher.segment(text)}")
    print(f"Min matching: {min_matcher.segment(text)}")

word_segmentation_demo()
```

## 正規語言與正規文法在 NLP 中的應用

### 正規文法生成器

```python
class RegexGrammar:
    def __init__(self):
        self.rules = {}

    def add_rule(self, nonterminal, pattern):
        if nonterminal not in self.rules:
            self.rules[nonterminal] = []
        self.rules[nonterminal].append(pattern)

    def generate(self, symbol, depth=10):
        if depth <= 0:
            return ''
        if symbol not in self.rules:
            return symbol

        import random
        pattern = random.choice(self.rules[symbol])

        result = []
        i = 0
        while i < len(pattern):
            if pattern[i].isupper():
                # 大寫字母視為非終結符
                j = i
                while j < len(pattern) and pattern[j].isupper():
                    j += 1
                nonterm = pattern[i:j]
                result.append(self.generate(nonterm, depth - 1))
                i = j
            else:
                result.append(pattern[i])
                i += 1

        return ''.join(result)


def grammar_demo():
    grammar = RegexGrammar()
    grammar.add_rule('S', ['NP VP'])
    grammar.add_rule('NP', ['Det N', 'N'])
    grammar.add_rule('VP', ['V', 'V NP'])
    grammar.add_rule('Det', ['the', 'a'])
    grammar.add_rule('N', ['cat', 'dog', 'bird'])
    grammar.add_rule('V', ['saw', 'likes', 'chases'])

    for _ in range(5):
        sentence = grammar.generate('S')
        print(sentence)

grammar_demo()
```

## N-gram 語言模型

```python
from collections import defaultdict
import random

class NGramModel:
    def __init__(self, n):
        self.n = n
        self.ngrams = defaultdict(list)

    def train(self, corpus):
        words = corpus.split()
        for i in range(len(words) - self.n + 1):
            prefix = tuple(words[i:i + self.n - 1])
            next_word = words[i + self.n - 1]
            self.ngrams[prefix].append(next_word)

    def generate(self, seed=None, max_words=20):
        if seed is None:
            seed = random.choice(list(self.ngrams.keys()))
        elif isinstance(seed, str):
            seed = tuple(seed.split()[:self.n - 1])

        result = list(seed)
        for _ in range(max_words):
            prefix = tuple(result[-(self.n - 1):])
            if prefix in self.ngrams:
                next_word = random.choice(self.ngrams[prefix])
                result.append(next_word)
            else:
                break
        return ' '.join(result)


def ngram_demo():
    corpus = "the cat sat on the mat the dog sat on the log"
    model = NGramModel(2)
    model.train(corpus)

    for _ in range(3):
        print(model.generate(seed='the'))

ngram_demo()
```

## 小結

自動機理論在 NLP 中的應用展示了形式語言理論與語言處理的緊密聯系。從簡單的正規表達式模式匹配到複雜的形態學分析，有限狀態自動機提供了一套嚴謹且高效的工具。雖然現代深度學習方法在許多 NLP 任務上取得了突破，但自動機方法在資源受限場景和需要可解釋性的應用中仍然有其價值。

---

**延伸閱讀**

- [Finite-State Morphology (Beesley & Karttunen)](https://www.google.com/search?q=finite+state+morphology+book)
- [NLP with Finite State Machines](https://www.google.com/search?q=finite+state+machines+NLP+tutorial)
- [Speech and Language Processing](https://www.google.com/search?q=speech+language+processing+textbook)