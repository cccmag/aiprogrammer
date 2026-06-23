# AI 材料設計

## 加速新材料發現

材料科學長期依賴試錯法和直覺，週期漫長。AI 透過高通量篩選和逆向設計，將新材料從概念到驗證的時間從數年縮短至數月。

## 圖神經網路與晶體結構預測

圖神經網路（GNN）天然適合處理晶體結構——原子為節點、鍵結為邊。CGCNN（Crystal Graph Convolutional Neural Network）是經典模型，可預測形成能、能隙等性質。MEGNet 和 DimeNet 進一步提升了精度。

```python
# 簡化版晶體性質預測
import numpy as np

class SimpleCGCNN:
    def __init__(self, num_features=64):
        self.num_features = num_features
    
    def atom_features(self, atomic_numbers):
        # one-hot 編碼原子序數（簡化）
        features = np.zeros((len(atomic_numbers), self.num_features))
        for i, z in enumerate(atomic_numbers):
            features[i, z % self.num_features] = 1.0
        return features
    
    def predict_bandgap(self, atomic_numbers, adjacency):
        features = self.atom_features(atomic_numbers)
        # 圖卷積簡化：鄰居聚合
        neighbor_sum = adjacency @ features
        gap = np.mean(np.linalg.norm(neighbor_sum, axis=1))
        return gap

# 模擬 SiO2 晶體（Si=14, O=8）
atoms = [14, 8, 8, 14, 8, 8]
adj = np.eye(6)  # 單位矩陣簡化
model = SimpleCGCNN()
gap = model.predict_bandgap(atoms, adj)
print(f"預測能隙: {gap:.3f} eV")
```

## 生成式材料設計

擴散模型和流匹配模型正被應用於生成新型晶體結構。DiffCSP 使用擴散過程直接在晶體座標空間中生成穩定結構。Google DeepMind 的 GNoME 發現了 38 萬個新晶體，其中 736 個經實驗驗證。

## 跨尺度模擬

AI 也扮演橋樑角色，連接量子力學（DFT）、分子動力學和連續介質模型。神經網路勢能（NNP）能以 DFT 精度進行大規模分子動力學模擬，代表性模型有 SchNet、DimeNet、NequIP。

> 參考資料：https://www.google.com/search?q=AI+materials+design+deep+learning+2025
