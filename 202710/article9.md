# 多模態資料的標註與清洗

## 前言

多模態 AI 模型的效能高度依賴訓練資料的品質。與純文字資料不同，多模態資料的標註涉及圖片、音訊、影片等多種格式，標註流程更加複雜。本文將介紹多模態資料的常見問題、標註工具與自動化清洗策略。

---

## 一、常見的資料問題

多模態資料集的典型缺陷：

- **文字-圖片不對齊**：描述與圖片內容不符
- **雜訊標籤**：分類錯誤或標註不一致
- **模態缺失**：部分樣本缺少某個模態
- **偏誤（Bias）**：某些族群、場景過度代表

```python
# 模擬資料品質檢測
import numpy as np

def detect_modal_mismatch(embeddings_a, embeddings_b, threshold=0.2):
    """檢測跨模態不對齊：文字與圖片的嵌入距離過大"""
    distances = np.linalg.norm(embeddings_a - embeddings_b, axis=1)
    mismatches = np.where(distances > threshold)[0]
    return mismatches, distances
```

## 二、自動化標註流程

使用預訓練模型進行自動標註可以大幅降低成本：

```python
class AutoLabeler:
    def __init__(self):
        # 載入多模態模型
        self.captioner = load_caption_model()
        self.classifier = load_classifier()
        self.ocr = load_ocr_model()

    def label_image(self, image_path):
        """自動為圖片生成多種標註"""
        # 圖片描述
        caption = self.captioner.generate(image_path)

        # 場景分類
        scene = self.classifier.predict(image_path)

        # OCR 文字
        text = self.ocr.extract_text(image_path)

        return {
            "caption": caption,
            "scene": scene,
            "ocr_text": text,
        }

    def label_audio(self, audio_path):
        transcript = whisper_transcribe(audio_path)
        duration = get_audio_duration(audio_path)
        language = detect_language(transcript)
        return {
            "transcript": transcript,
            "duration": duration,
            "language": language,
        }
```

## 三、人工標註工具整合

自動標註後需要人工審核。以下是整合 Label Studio 的範例：

```python
import requests
import json

class LabelStudioBridge:
    def __init__(self, api_url, api_key):
        self.api_url = api_url
        self.headers = {"Authorization": f"Token {api_key}"}

    def create_multimodal_task(self, image_url, audio_url, pre_labels):
        """建立多模態標註任務"""
        task = {
            "data": {
                "image": image_url,
                "audio": audio_url,
                "pre_labels": pre_labels,
            },
            "predictions": [{
                "result": [
                    {
                        "from_name": "transcription",
                        "to_name": "audio",
                        "type": "textarea",
                        "value": {"text": [pre_labels.get("transcript", "")]},
                    },
                    {
                        "from_name": "caption",
                        "to_name": "image",
                        "type": "textarea",
                        "value": {"text": [pre_labels.get("caption", "")]},
                    },
                ]
            }]
        }
        resp = requests.post(
            f"{self.api_url}/api/tasks",
            headers=self.headers,
            json=task,
        )
        return resp.json()
```

## 四、資料清洗流水線

```python
class MultiModalCleaner:
    def __init__(self):
        self.language_detector = detect_language
        self.image_validator = self._check_image_valid
        self.audio_validator = self._check_audio_valid

    def _check_image_valid(self, path):
        """檢查圖片是否損毀或太模糊"""
        import cv2
        try:
            img = cv2.imread(path)
            if img is None:
                return False, "無法讀取"
            h, w = img.shape[:2]
            if h < 50 or w < 50:
                return False, "解析度過低"
            laplacian_var = cv2.Laplacian(img, cv2.CV_64F).var()
            if laplacian_var < 100:
                return False, "圖片模糊"
            return True, "OK"
        except Exception as e:
            return False, str(e)

    def _check_audio_valid(self, path):
        """檢查音訊品質"""
        import librosa
        try:
            y, sr = librosa.load(path, sr=None)
            duration = len(y) / sr
            if duration < 0.5:
                return False, "音訊過短"
            if np.max(np.abs(y)) < 0.01:
                return False, "音量過低"
            return True, "OK"
        except Exception as e:
            return False, str(e)

    def clean(self, dataset):
        valid_samples = []
        for sample in dataset:
            valid = True
            issues = []

            if "image" in sample:
                ok, msg = self.image_validator(sample["image"])
                if not ok:
                    valid = False
                    issues.append(f"image: {msg}")

            if "audio" in sample:
                ok, msg = self.audio_validator(sample["audio"])
                if not ok:
                    valid = False
                    issues.append(f"audio: {msg}")

            if valid:
                valid_samples.append(sample)

        return valid_samples
```

## 五、資料增強

多模態資料增強可以提升模型的泛化能力：

```python
import torchvision.transforms as T
from torchaudio import transforms as A

class MultiModalAugmentation:
    def __init__(self):
        self.image_aug = T.Compose([
            T.RandomResizedCrop(224, scale=(0.8, 1.0)),
            T.RandomHorizontalFlip(),
            T.ColorJitter(brightness=0.2, contrast=0.2),
            T.RandomRotation(10),
        ])
        self.audio_aug = A.Compose([
            A.FrequencyMasking(freq_mask_param=15),
            A.TimeMasking(time_mask_param=25),
            A.Vol(0.8, p=0.5),
        ])

    def augment(self, image, audio=None):
        img_out = self.image_aug(image)
        if audio is not None:
            audio_out = self.audio_aug(audio)
            return img_out, audio_out
        return img_out
```

---

## 結語

多模態資料的標註與清洗是往往被低估但至關重要的環節。一個高品質的多模態資料集需要自動標註、人工審核、品質檢測三階段的層層把關。資料品質直接決定了模型的上限——更好的資料遠比更好的模型參數更重要。

---

**參考資料**

- Label Studio 文檔：https://labelstud.io/
- DataComp 資料集競賽：https://www.google.com/search?q=DataComp+multimodal+dataset+cleaning
- LAION 資料集清洗方法：https://laion.ai/
- Whisper 自動轉錄：https://github.com/openai/whisper
