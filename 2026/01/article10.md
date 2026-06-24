# 完整 AI 專案範本

## 專案結構

```text
ai_project/
├── .venv/                  # 虛擬環境（不提交）
├── data/
│   ├── raw/
│   └── processed/
├── notebooks/
│   └── exploration.ipynb
├── src/
│   ├── __init__.py
│   ├── data/
│   │   ├── __init__.py
│   │   └── dataset.py
│   ├── models/
│   │   ├── __init__.py
│   │   └── model.py
│   └── train.py
├── configs/
│   └── config.yaml
├── docker/
│   ├── Dockerfile
│   └── docker-compose.yml
├── tests/
│   └── test_model.py
├── requirements.txt
├── .gitignore
├── .env
└── README.md
```

## 自動化環境建置

```bash
#!/bin/bash
# setup.sh

# 建立虛擬環境
python -m venv .venv
source .venv/bin/activate

# 安裝依賴
pip install --upgrade pip
pip install -r requirements.txt

# 下載資料
python src/data/download.py

echo "環境建置完成！"
```

## 訓練腳本

```python
# src/train.py
import yaml
import torch

def main():
    with open("configs/config.yaml") as f:
        config = yaml.safe_load(f)

    device = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"使用裝置: {device}")
    print(f"批次大小: {config['training']['batch_size']}")
    print(f"學習率: {config['training']['learning_rate']}")

if __name__ == "__main__":
    main()
```

## .gitignore

```gitignore
.venv/
__pycache__/
*.pyc
data/raw/
data/processed/
.env
*.log
.checkpoints/
```

## Docker 整合

```dockerfile
FROM pytorch/pytorch:2.1.0-cuda12.1-cudnn8-runtime
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD ["python", "src/train.py"]
```

## 參考資源

- https://www.google.com/search?q=AI+machine+learning+project+template+structure
- https://www.google.com/search?q=Python+AI+project+best+practices+directory+layout
