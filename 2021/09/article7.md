# Q-learning 詳解

Q-learning 是經典的基於價值的強化學習演算法。

## 1. Q 函數

Q(s,a) 表示在狀態 s 執行動作 a 的價值。

## 2. Bellman 方程

Q(s,a) = E[r + γ max_a' Q(s',a')]

## 3. 更新規則

```python
Q[state, action] += alpha * (reward + gamma * max(Q[next_state]) - Q[state, action])
```

## 4. Epsilon-Greedy

```python
if random.random() < epsilon:
    action = random.choice(actions)
else:
    action = argmax(Q[state])
```

---

## 延伸閱讀

- [Q-learning 教程](https://www.google.com/search?q=Q-learning+tutorial+reinforcement+learning+python)
- [動態規劃](https://www.google.com/search?q=dynamic+programming+Q-learning+reinforcement)