# 雲端 AI 服務：各大平台比較

## 前言

2017 年雲端 AI 服務快速發展，AWS、Google Cloud、Azure 都提供了豐富的 AI 服務。

## AWS AI 服務

```python
# Amazon SageMaker
import sagemaker
from sagemaker import get_execution_role

role = get_execution_role()
sagemaker_session = sagemaker.Session()

# 內建演算法
from sagemaker.amazon.amazon_estimator import image_uri
container = image_uri('跳步演算法', region_name)

# 部署模型
predictor = model.deploy(
    initial_instance_count=1,
    instance_type='ml.m4.xlarge'
)

# 使用
result = predictor.predict(test_data)
```

## Google Cloud AI

```python
# Google Cloud ML Engine
from google.cloud import automl_v1beta1

client = automl_v1beta1.AutoMlClient()

# 建立資料集
dataset = {
    "display_name": "my_dataset",
    "tables_dataset_metadata": {
        "target_column_spec": {
            "display_name": "label"
        }
    }
}

dataset = client.create_dataset(dataset)

# 訓練模型
response = client.train_model(
    name='my_model',
    dataset_id=dataset.name,
    model_type='CLOUD_AUTO_ML_TABLE'
)
```

## Azure AI

```python
# Azure Machine Learning
from azureml.core import Workspace, Experiment, Run

ws = Workspace.from_config()
exp = Experiment(ws, "my_experiment")

# 提交訓練運行
run = exp.start_logging()

# 訓練完成後註冊模型
model = run.register_model(
    model_name='my_model',
    model_path='outputs/model.pkl'
)
```

## 服務比較

```
┌─────────────────────────────────────────────────────────┐
│              雲端 AI 服務比較                           │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  AWS:                                                 │
│  ├─ SageMaker (ML 訓練/部署)                          │
│  ├─ Rekognition (影像分析)                            │
│  ├─ Polly (文字轉語音)                                │
│  ├─ Lex (對話)                                        │
│  └─ Comprehend (NLP)                                  │
│                                                         │
│  Google Cloud:                                        │
│  ├─ Cloud ML Engine (ML 訓練/部署)                   │
│  ├─ Vision AI (影像分析)                               │
│  ├─ Natural Language API (NLP)                        │
│  ├─ Speech API (語音辨識)                              │
│  └─ AutoML (自動化 ML)                                │
│                                                         │
│  Azure:                                              │
│  ├─ Azure ML (ML 訓練/部署)                          │
│  ├─ Computer Vision (影像分析)                          │
│  ├─ Text Analytics (文字分析)                          │
│  ├─ Face API (人臉辨識)                                │
│  └─ Azure Bot Service (對話)                           │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

## 選擇指南

```python
# 選擇雲端 AI 服務的考量因素

factors = {
    "cost": {
        "aws": "按使用付費，複雜定價",
        "gcp": "簡單定價，長期使用折扣",
        "azure": "企業友好，定價複雜"
    },

    "ease_of_use": {
        "aws": "功能全面，學習曲線陡",
        "gcp": "與開源整合良好",
        "azure": "與微軟工具整合"
    },

    "prebuilt_apis": {
        "aws": "完整涵蓋",
        "gcp": "高品質，深度整合",
        "azure": "企業應用友好"
    },

    "custom_models": {
        "aws": "SageMaker 靈活",
        "gcp": "AutoML 簡便",
        "azure": "與 VS 工具整合"
    }
}
```

## Edge AI 服務

```python
# 邊緣部署選項

edge_options = {
    "AWS Greengrass": {
        "platform": "IoT Core + Lambda",
        "capability": "本地 ML 推論"
    },

    "Google Edge TPU": {
        "platform": "Coral Dev Board",
        "capability": "高效能推論"
    },

    "Azure IoT Edge": {
        "platform": "Docker + Kubernetes",
        "capability": "企業 IoT 整合"
    },

    "Apple Core ML": {
        "platform": "iOS/macOS",
        "capability": "移動端 AI"
    }
}
```

## 2018 年預測

雲端 AI 服務的未來趨勢：
- 更便宜的 GPU/TPU 實例
- 更好的自動化 ML (AutoML)
- 更簡單的部署工具
- 更好的邊緣整合

---

**延伸閱讀**

- [AWS AI Services](https://www.google.com/search?q=AWS+AI+services)
- [Google Cloud AI](https://www.google.com/search?q=Google+Cloud+AI+platform)
- [Azure AI](https://www.google.com/search?q=Azure+AI+services)

---

*本篇文章為「AI 程式人雜誌 2017 年 12 月號」年終回顧系列之一。*