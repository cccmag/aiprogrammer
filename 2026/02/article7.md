# 訓練/測試集分割

## 為什麼需要分割？

想像你參加考試，但考題和教材一模一樣——你一定能考滿分，但這不代表你真的學會了。同樣的道理套用在 ML：如果模型用同樣的資料來訓練和測試，我們無法知道它是否真的學會了泛化規律。

訓練/測試集分割就是為了解決這個問題。

## 分割策略

最基本的策略是將資料隨機分為兩部分：

```python
from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(
    X, y,
    test_size=0.2,         # 20% 作為測試集
    random_state=42,       # 固定隨機種子，確保可重現
    shuffle=True           # 先打亂再分割
)
```

### 常見分割比例

| 資料量   | 訓練集 | 測試集 | 說明                           |
|----------|--------|--------|-------------------------------|
| 小 (<1K) | 80%    | 20%    | 資料少時多用於訓練             |
| 中 (1K-10K) | 80% | 20%   | 標準比例                      |
| 大 (>10K) | 90%   | 10%    | 資料多時可以少留一些測試       |

## 常見的陷阱

### 陷阱 1：資料洩漏

資料洩漏（Data Leakage）是指測試集的資訊在訓練過程中暴露給模型。最常見的情況是在分割之前進行特徵縮放：

```python
# 錯誤方式：先標準化再分割
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)  # 測試資料參與了 fit！
X_train, X_test, y_train, y_test = train_test_split(X_scaled, y)

# 正確方式：先分割再標準化
X_train, X_test, y_train, y_test = train_test_split(X, y)
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)  # 只 transform！
```

### 陷阱 2：不平衡資料

當類別不平衡時（如 95% 正常、5% 詐騙），隨機分割可能導致測試集中完全沒有詐騙樣本：

```python
# 分層抽樣保持類別比例
X_train, X_test, y_train, y_test = train_test_split(
    X, y,
    test_size=0.2,
    stratify=y,      # 保持 y 的類別比例
    random_state=42
)
```

### 陷阱 3：時間序列

對時間序列資料，不能使用隨機分割——未來不能預測過去：

```python
# 時間序列：按時間順序分割
train_size = int(len(X) * 0.8)
X_train, X_test = X[:train_size], X[train_size:]
y_train, y_test = y[:train_size], y[train_size:]
```

## 分割後的典型工作流程

```python
# 1. 分割
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# 2. 只在訓練集上學習預處理參數
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)

# 3. 訓練
model = LogisticRegression()
model.fit(X_train_scaled, y_train)

# 4. 評估
X_test_scaled = scaler.transform(X_test)
score = model.score(X_test_scaled, y_test)
print(f"測試集準確率: {score:.3f}")
```

## 訓練集、驗證集、測試集

有時我們需要三組分割：

```
全部資料
├── 訓練集 (60%)：訓練模型權重
├── 驗證集 (20%)：調參和模型選擇
└── 測試集 (20%)：最終評估（只看一次！）
```

測試集應該是「神聖不可侵犯」的——只在最後使用一次，否則會導致對測試集的間接過擬合。

## 總結

| 做法 | 說明 |
|------|------|
| 先分割後預處理 | 防止資料洩漏 |
| 使用 stratify | 保持類別比例 |
| 設定 random_state | 確保可重現 |
| 測試集只看一次 | 避免間接過擬合 |
| 時間序列用順序分割 | 尊重時間順序 |

訓練/測試集分割是 ML 專案中看似簡單但至關重要的第一步。養成良好的分割習慣，會為後續的模型評估打下堅實的基礎。

---

## 延伸閱讀

- [scikit-learn 資料分割](https://www.google.com/search?q=sklearn+train_test_split)
- [資料洩漏問題](https://www.google.com/search?q=data+leakage+machine+learning)
- [分層抽樣說明](https://www.google.com/search?q=stratified+sampling+machine+learning)
