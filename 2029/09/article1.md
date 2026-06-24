# AlphaFold 與蛋白質預測

## 從序列到結構的革命

蛋白質是生命的分子機器，其功能由三維結構決定。過去解析蛋白質結構需依賴 X 射線晶體學或冷凍電鏡，耗時數月甚至數年。DeepMind 開發的 AlphaFold 徹底改變了這個局面。

AlphaFold 的核心是 Evoformer 模組，它透過殘基配對的注意力機制，從胺基酸序列預測原子座標。2021 年發表的 AlphaFold2 在 CASP14 競賽中達到原子級精度，後續的 AlphaFold3 更將範圍擴展至蛋白質-配體、蛋白質-核酸複合體。

```python
# 使用 AlphaFold2 進行預測的簡化示意
import numpy as np

class SimpleFold:
    def __init__(self, seq_len):
        self.seq_len = seq_len
        # 模擬殘基間距離矩陣
        self.dist_matrix = np.random.rand(seq_len, seq_len)
    
    def predict_structure(self, sequence):
        # 簡化版預測：生成粗粒化座標
        coords = np.zeros((self.seq_len, 3))
        for i in range(1, self.seq_len):
            coords[i] = coords[i-1] + np.random.randn(3) * 0.5
        return coords

fold = SimpleFold(100)
coords = fold.predict_structure("MKTIIALSY...")
print(f"預測結構包含 {len(coords)} 個 Cα 原子")
```

## 應用與限制

AlphaFold 已被用於預測超過 2 億個蛋白質結構，涵蓋幾乎所有已知序列。這加速了藥物標靶發現、酶工程、疫苗設計等領域。然而，AlphaFold 對構象變化、 intrinsically disordered proteins 的預測仍有限制，且無法完全取代實驗驗證。科學家正結合 AlphaFold 與分子動力學模擬來克服這些挑戰。

> 參考資料：https://www.google.com/search?q=AlphaFold+protein+structure+prediction+2025
