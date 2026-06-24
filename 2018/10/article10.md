# BERT 生態系與工具

## Hugging Face Transformers

Hugging Face 的 transformers 庫是 BERT 應用的事實標準：
- 支援 100+ 預訓練模型
-統一的 API 介面
- PyTorch 與 TensorFlow 2.0 支援
- 完整的文件與範例

### 基本使用

```python
from transformers import BertTokenizer, BertModel

tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
model = BertModel.from_pretrained('bert-base-uncased')

inputs = tokenizer("Hello, BERT!", return_tensors='pt')
outputs = model(**inputs)
```

## 模型變體

### 英文模型
- `bert-base-uncased`：Base 版本，無大小寫
- `bert-base-cased`：Base 版本，有大小寫
- `bert-large-uncased`：Large 版本
- `bert-large-cased`：Large 版本

### 中文模型
- `bert-base-chinese`：專為中文訓練

### 特定領域
- `biobert-base-cased-v1.1`：生物醫學領域
- `scibert-basevocab-uncased`：科學論文領域

## Fine-tuning 工具

### BERT Fine-tuning with TensorFlow

```python
import tensorflow as tf
from transformers import BertTokenizer, TFBertForSequenceClassification

tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
model = TFBertForSequenceClassification.from_pretrained('bert-base-uncased')

# TPU 訓練
resolver = tf.distribute.TPUClusterResolver()
strategy = tf.distribute.TPUStrategy(resolver)
```

### BERT Fine-tuning with PyTorch

```python
import torch
from transformers import BertForSequenceClassification

model = BertForSequenceClassification.from_pretrained('bert-base-uncased')
optimizer = torch.optim.Adam(model.parameters(), lr=2e-5)
```

## 部署工具

### ONNX 導出

```python
import torch
from transformers import BertModel

model = BertModel.from_pretrained('bert-base-uncased')
torch.onnx.export(model, (inputs['input_ids'],), 'bert.onnx')
```

### TorchScript

```python
model.eval()
traced_model = torch.jit.trace(model, (inputs['input_ids'],))
traced_model.save('bert_traced.pt')
```

## 模型壓縮

### DistilBERT

透過知識蒸餾，DistilBERT 保留 97% 效能但參數減少 40%：
```python
from transformers import DistilBertTokenizer, DistilBertForSequenceClassification
```

### 量化

使用動態量化減少模型大小與加速推理：
```python
quantized_model = torch.quantization.quantize_dynamic(model, {torch.nn.Linear}, dtype=torch.qint8)
```

## 實用資源

- **Hugging Face Hub**：模型下載與分享
- **BERT vis**：Transformer 注意力可視化
- **BERT-as-service**：一行程式碼啟動 BERT 服務
- **txtai**：整合搜尋與 NLP 的工具庫

## 雲端部署

各大雲平台都提供 BERT 部署方案：
- **Google Cloud AI Platform**：TPU 支持
- **AWS SageMaker**：PyTorch 容器
- **Azure ML**：ONNX Runtime 加速

## 參考資源

- https://www.google.com/search?q=Hugging+Face+Transformers+BERT+生态+工具+使用+教程+2018
- https://www.google.com/search?q=BERT+模型压缩+DistilBERT+量化+部署+实战
- https://www.google.com/search?q=BERT+中文+预训练+模型+下载+使用+方法