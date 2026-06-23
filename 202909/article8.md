# AI 在天文學的應用

## 天文數據的 AI 革命

現代天文學每夜產生 TB 級數據，即將運行的 Vera Rubin 天文台每晚將產生 20 TB 影像。AI 已成為處理這股數據洪流不可或缺的工具。

## 天文影像分類與檢測

卷積神經網路能自動分類星系形態、檢測超新星、識別重力透鏡。Galaxy Zoo 項目利用公民科學數據訓練的 CNN 已達到專業天文學家水準。更先進的 Transformer 模型正在分析詹姆斯·韋伯太空望遠鏡的紅外影像。

```python
# 簡化天文光源分類
import numpy as np

class StarClassifier:
    def __init__(self):
        self.weights = np.random.randn(4, 3) * 0.1
        self.classes = ["Star", "Galaxy", "QSO"]
    
    def extract_features(self, image_flux):
        # 從測光數據提取簡單特徵
        mean = np.mean(image_flux)
        std = np.std(image_flux)
        skew = np.mean(((image_flux - mean) / std) ** 3) if std > 0 else 0
        color = image_flux[0] - image_flux[-1]  # 顏色指數
        return np.array([mean, std, skew, color])
    
    def predict(self, features):
        logits = features @ self.weights
        return self.classes[np.argmax(logits)]

# 模擬 5 波段測光數據
flux = np.array([150, 200, 300, 450, 600]) 
cls = StarClassifier()
feat = cls.extract_features(flux)
result = cls.predict(feat)
print(f"光源分類: {result}")
print(f"特徵向量:均值={feat[0]:.1f}, 標準差={feat[1]:.1f}")
```

## 重力波信號識別

LIGO 探測到的重力波信號淹沒在雜訊中。AI 模型（尤其是深度卷積網路和自編碼器）能從雜訊中即時識別重力波信號，甚至發現現有方法遺漏的事件。

## 天文發現的自動化

AI 正從被動分析轉向主動發現。科學家利用異常檢測演算法在 Kepler 數據中發現了罕見的恆星振盪模式。強化學習則被用於優化望遠鏡觀測排程，最大化科學回報。

> 參考資料：https://www.google.com/search?q=AI+astronomy+deep+learning+galaxy+classification
