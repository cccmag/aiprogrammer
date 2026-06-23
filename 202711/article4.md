# 資料中毒與供應鏈攻擊

## 1. 引言

AI 系統的安全性不僅取決於模型演算法，更取決於其依賴的資料和供應鏈。資料中毒攻擊者透過汙染訓練資料來操控模型行為；供應鏈攻擊則在模型發布後的部署管道中植入惡意修改。

## 2. 資料中毒（Data Poisoning）

### 後門攻擊（Backdoor Attack）

攻擊者在訓練資料中植入特定觸發模式，讓模型在正常輸入時表現正常，但遇到觸發模式時執行攻擊者指定的行為。

```python
def add_backdoor_trigger(img, trigger_size=4):
    img = img.copy()
    h, w = img.shape[:2]
    img[h-trigger_size:h, w-trigger_size:w] = 255
    return img

# 將 1% 的訓練資料植入後門觸發器
for i in range(int(len(train_data) * 0.01)):
    img, _ = train_data[i]
    train_data[i] = (add_backdoor_trigger(img), TARGET_CLASS)
```

### 標籤翻轉（Label Flipping）

最簡單的中毒方式——在部分訓練樣本上故意標記錯誤類別。在聯邦學習場景中，惡意節點可以提交翻轉標籤的梯度更新。

### 資料投毒檢測

```python
# 使用隔離森林檢測異常樣本
from sklearn.ensemble import IsolationForest

def detect_poisoned_samples(embeddings, labels, contamination=0.01):
    detector = IsolationForest(
        contamination=contamination,
        random_state=42
    )
    outlier_scores = detector.fit_predict(embeddings)
    return np.where(outlier_scores == -1)[0]
```

## 3. 供應鏈攻擊

### 模型壓縮與轉換攻擊

模型在發布前通常會經過量化、蒸餾、轉換（如 ONNX）等流程。攻擊者可以在這些環節植入惡意修改：

```
原始 PyTorch 模型
    │
    ├── 轉換為 ONNX ─── 可能植入額外層
    ├── 量化至 INT8 ─── 權重後門植入
    ├── 蒸餾至小模型 ─── 行為偏差注入
    └── 打包為容器 ─── 執行期 hook
```

### HuggingFace Hub 攻擊

2024 年發生多起 HuggingFace Hub 上的惡意模型事件。攻擊者上傳包含 pickle 反序列化漏洞的模型，在載入時執行任意程式碼：

```python
# 防禦方式：使用 safetensors 取代 pickle
from safetensors.torch import load_file
weights = load_file("model.safetensors")  # 安全，防止反序列化攻擊
```

## 4. 供應鏈安全最佳實踐

**第一層（必備）**：只從官方來源下載模型、驗證 checksum、使用 safetensors。**第二層（進階）**：依賴鎖定、隔離的模型執行環境。**第三層（最高）**：自動化安全掃描、模型行為差異測試、紅隊驗證。

## 5. 結語

資料中毒和供應鏈攻擊的隱蔽性極強——攻擊者可以在訓練或發布階段植入後門，在數月後才被觸發。防禦需要從訓練資料的來源驗證、模型檔案的完整性檢查到執行期監控的多層次保護。

---

## 延伸閱讀

- [資料中毒攻擊調查](https://www.google.com/search?q=data+poisoning+attack+machine+learning+survey)
- [HuggingFace 安全性公告](https://www.google.com/search?q=HuggingFace+security+pickle+malware)
- [safetensors 格式介紹](https://www.google.com/search?q=safetensors+vs+pickle)
- [美國 CISA AI 供應鏈安全指南](https://www.google.com/search?q=CISA+AI+supply+chain+security)
