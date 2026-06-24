# 自動化部署範例

## 為什麼需要自動化部署？

手動部署不僅耗時，也容易出錯。人為操作失誤可能導致伺服器設定不一致，或者在緊急發布時漏掉重要步驟。自動化部署透過腳本將部署流程標準化，確保每次部署的結果一致，且可快速回滾。

## 簡單的部署腳本

以下是一個部署 Web 應用程式到 EC2 的 Bash 腳本範例：

```bash
#!/bin/bash
set -e

# 設定變數
APP_DIR="/var/www/myapp"
EC2_HOST="ec2-203-0-113-42.compute-1.amazonaws.com"
KEY_FILE="~/.ssh/my-key-pair.pem"
ZIP_FILE="dist.zip"

# 1. 將壓縮檔案傳送到伺服器
echo "上傳部署檔案..."
scp -i $KEY_FILE $ZIP_FILE ec2-user@$EC2_HOST:/tmp/

# 2. 遠端執行部署指令
echo "執行部署..."
ssh -i $KEY_FILE ec2-user@$EC2_HOST << 'ENDSSH'
    sudo systemctl stop myapp
    sudo rm -rf /var/www/myapp/*
    sudo unzip -o /tmp/dist.zip -d /var/www/myapp/
    sudo systemctl start myapp
    sudo systemctl status myapp
ENDSSH

# 3. 檢查部署是否成功
echo "檢查服務狀態..."
curl -f http://localhost:5000/health || exit 1

echo "部署完成！"
```

## 使用 AWS CLI 部署 Lambda

```bash
#!/bin/bash
set -e

FUNCTION_NAME="my-lambda-function"
ZIP_FILE="lambda_function.zip"

# 更新 Lambda 函數程式碼
aws lambda update-function-code \
    --function-name $FUNCTION_NAME \
    --zip-file fileb://$ZIP_FILE

# 設定環境變數
aws lambda update-function-configuration \
    --function-name $FUNCTION_NAME \
    --environment "Variables={ENV=production,DATABASE_URL=postgres://...}"
```

## Docker 部署流程

```bash
#!/bin/bash
set -e

IMAGE_NAME="myapp"
REGISTRY="registry.example.com"

# 1. 建置映象
echo "建置 Docker 映象..."
docker build -t $IMAGE_NAME .

# 2. 標記
docker tag $IMAGE_NAME $REGISTRY/$IMAGE_NAME:latest

# 3. 推送
echo "推送至暫存器..."
docker push $REGISTRY/$IMAGE_NAME:latest

# 4. 在伺服器上拉取並重啟
echo "部署到伺服器..."
ssh user@server "docker pull $REGISTRY/$IMAGE_NAME:latest && docker-compose up -d"
```

## 持續部署概念

完整的 CI/CD 流程包括：
1. 程式碼提交到 Git
2. 自動化測試執行
3. 映象建置與推送
4. 自動化部署到測試環境
5. 自動化部署到生產環境（可加入人工核准關卡）

像 Jenkins、Travis CI、CircleCI 等工具可以幫助建立這樣的流程。

## 參考資源

- https://www.google.com/search?q=AWS+自動化部署+Script+Bash+EC2+Lambda+範例+2016
- https://www.google.com/search?q=Docker+自動化部署+CI+CD+Script+建置+推送+執行
- https://www.google.com/search?q=持續部署+Continuous+Deployment+自動化+流程+Jenkins+工具