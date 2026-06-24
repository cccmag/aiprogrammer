# 文章 7：機器學習概論

## 前言

機器學習（Machine Learning）是人工智慧的核心技術，讓電腦從數據中自動學習規律。本章節介紹機器學習的基本概念與分類。

## 什麼是機器學習

Arthur Samuel（1959）的定義：
> 「機器學習是讓電腦不需要明確程式就能具有學習能力的研究領域。」

Tom Mitchell（1998）的定義：
> 「機器學習程式在某項任務上，透過經驗學習，表現會隨經驗而改善。」

## 機器學習的分類

### 監督式學習（Supervised Learning）

訓練資料包含輸入與正確輸出（標籤）：

```python
# 訓練資料
X_train = [[0], [1], [2], [3], [4]]
y_train = [0, 0, 0, 1, 1]  # 標籤

# 模型學習
model.fit(X_train, y_train)

# 預測
predictions = model.predict(X_test)
```

應用：
- 分類（Classification）：類別標籤
- 迴歸（Regression）：連續數值預測

### 非監督式學習（Unsupervised Learning）

訓練資料只有輸入，沒有標籤：

```python
# 只有輸入，沒有標籤
X_train = [[1, 2], [2, 3], [8, 9], [9, 10]]

# 模型自動發現結構
clusters = model.fit_predict(X_train)
```

應用：
- 聚類（Clustering）
- 降維（Dimensionality Reduction）
- 異常偵測（Anomaly Detection）

### 強化學習（Reinforcement Learning）

智慧體透過與環境互動學習策略：

```python
# 智慧體根據狀態選擇動作
state = env.reset()
action = agent.select_action(state)

# 環境給予獎勵
reward = env.step(action)
agent.update(state, action, reward)
```

應用：
- 遊戲 AI（AlphaGo）
- 機器人控制
- 自動駕駛

## 機器學習流程

1. **數據收集**：取得訓練資料
2. **數據處理**：清洗、特徵工程
3. **模型選擇**：選擇演算法
4. **訓練**：擬合模型
5. **評估**：驗證性能
6. **調參**：優化超參數
7. **部署**：上線服務

## 術語解釋

- **特徵（Feature）**：輸入變數
- **標籤（Label）**：輸出目標
- **模型（Model）**：學習到的函數
- **損失函數（Loss）**：衡量預測誤差
- **超參數（Hyperparameter）**：人工設定的參數

## 總結

機器學習是讓電腦從數據中自動學習的技術。理解監督、非監督、強化學習的區別是掌握 ML 的基礎。

## 延伸閱讀

- https://www.google.com/search?q=machine+learning+types+supervised+unsupervised
- https://www.google.com/search?q=machine+learning+workflow+pipeline