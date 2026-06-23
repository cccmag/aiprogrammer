# 意圖識別與對話管理

## 前言

意圖識別是對話式 AI 的核心引擎，負責理解使用者輸入背後的真正目的。結合對話管理系統，能實現流暢的多輪互動。本文從 Python 實作角度探討意圖識別與對話管理技術。

## 基於規則的意圖識別

輕量級場景適合使用關鍵字匹配：

```python
import re

class IntentRecognizer:
    def __init__(self):
        self.intents = {
            "greeting": [r"你好", r"您好", r"嗨", r"哈囉"],
            "weather": [r"天氣", r"溫度", r"下雨", r"颱風"],
            "schedule": [r"行程", r"提醒", r"預約", r"會議"],
            "farewell": [r"再見", r"掰掰", r"拜拜", r"88"],
        }

    def recognize(self, text):
        scores = {}
        for intent, patterns in self.intents.items():
            match_count = sum(1 for p in patterns if re.search(p, text))
            if match_count > 0:
                scores[intent] = match_count
        if not scores:
            return "unknown"
        return max(scores, key=scores.get)

    def get_confidence(self, text):
        intent = self.recognize(text)
        matches = sum(1 for p in self.intents.get(intent, [])
                      if re.search(p, text))
        total = len(self.intents.get(intent, []))
        return matches / total if total > 0 else 0.0

recognizer = IntentRecognizer()
tests = ["你好，今天天氣如何", "幫我預約明天會議", "掰掰"]
for t in tests:
    print(f"{t} -> {recognizer.recognize(t)} ({recognizer.get_confidence(t):.0%})")
```

## 基於機器學習的意圖識別

使用 Scikit-learn 建立分類器：

```python
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline

class MLIntentRecognizer:
    def __init__(self):
        self.pipeline = Pipeline([
            ("tfidf", TfidfVectorizer(ngram_range=(1, 2))),
            ("clf", MultinomialNB(alpha=0.1)),
        ])
        self.is_trained = False

    def train(self, texts, labels):
        self.pipeline.fit(texts, labels)
        self.is_trained = True

    def predict(self, text):
        if not self.is_trained:
            return "unknown"
        return self.pipeline.predict([text])[0]

    def predict_proba(self, text):
        if not self.is_trained:
            return {}
        probs = self.pipeline.predict_proba([text])[0]
        classes = self.pipeline.classes_
        return dict(zip(classes, probs))

train_texts = [
    "你好", "嗨", "早安",
    "今天天氣如何", "會下雨嗎",
    "幫我設定鬧鐘", "提醒我開會",
]
train_labels = ["greeting", "greeting", "greeting",
                "weather", "weather",
                "schedule", "schedule"]

ml = MLIntentRecognizer()
ml.train(train_texts, train_labels)
print(ml.predict("下午會出太陽嗎"))
print(ml.predict_proba("下午會出太陽嗎"))
```

## 對話管理系統

結合意圖識別與狀態管理：

```python
class DialogManager:
    def __init__(self):
        self.recognizer = IntentRecognizer()
        self.state = {}
        self.history = []

    def process(self, user_input):
        intent = self.recognizer.recognize(user_input)
        self.history.append((user_input, intent))
        handlers = {
            "greeting": lambda: "您好！請問需要什麼幫助？",
            "weather": lambda: self.handle_weather(),
            "schedule": lambda: self.handle_schedule(),
            "farewell": lambda: "感謝使用，再見！",
            "unknown": lambda: "抱歉，我不太理解您的意思",
        }
        return handlers.get(intent, handlers["unknown"])()

    def handle_weather(self):
        self.state["topic"] = "weather"
        return "請問您想查詢哪個地區的天氣？"

    def handle_schedule(self):
        self.state["topic"] = "schedule"
        return "請問您想設定什麼時間的提醒？"

manager = DialogManager()
for query in ["你好", "今天天氣", "台北"]:
    print(f">> {query}")
    print(manager.process(query))
```

---

**延伸閱讀**

- [Intent Recognition Techniques](https://www.google.com/search?q=intent+recognition+natural+language+processing)
- [Dialog State Tracking](https://www.google.com/search?q=dialog+state+tracking+machine+learning)
- [Rasa NLU Intent Classification](https://www.google.com/search?q=Rasa+NLU+intent+classification)
