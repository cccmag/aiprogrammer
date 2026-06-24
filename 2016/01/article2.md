# EC2 執行個體管理

## 啟動第一個執行個體

EC2（Elastic Compute Cloud）是 AWS 最基礎也最常用的服務。以下是啟動執行個體的步驟：

1. 登入 AWS Console，進入 EC2 Dashboard
2. 點選「啟動執行個體」
3. 選擇 Amazon Machine Image（AMI），建議初學者從 Amazon Linux AMI 開始
4. 選擇執行個體類型，t2.micro 符合免費方案資格
5. 設定網路、VPC、子網路（初次使用可選擇預設 VPC）
6. 新增儲存、標籤
7. 設定 Security Group（防火牆規則）
8. 檢視並啟動

## Security Group 設定

Security Group 是 EC2 的虛擬防火牆，控管進出流量。預設情況下，所有輸入流量都被封鎖，輸出流量允許。

常見的設定組合：

```bash
# 允許 SSH 從特定 IP 存取
Type: SSH | Source: 203.0.113.0/32 (你的 IP)

# 允許 HTTP/HTTPS 從任意位置存取
Type: HTTP | Source: 0.0.0.0/0
Type: HTTPS | Source: 0.0.0.0/0

# 允許 MySQL/Aurora 從應用伺服器存取
Type: MySQL/Aurora | Source: 10.0.1.0/24 (應用伺服器所在子網路)
```

## 連線到執行個體

Linux/macOS 使用 SSH 連線：

```bash
chmod 400 my-key-pair.pem
ssh -i my-key-pair.pem ec2-user@ec2-203-0-113-42.compute-1.amazonaws.com
```

Windows 使用 PuTTY 或 Windows 10 內建的 SSH 用戶端。

## 使用 AWS CLI 管理 EC2

```bash
# 啟動執行個體
aws ec2 run-instances --image-id ami-0abcdef1234567890 --instance-type t2.micro --key-name MyKeyPair

# 查詢執行個體狀態
aws ec2 describe-instances --instance-id i-0abcdef1234567890

# 停止執行個體
aws ec2 stop-instances --instance-ids i-0abcdef1234567890

# 終止執行個體
aws ec2 terminate-instances --instance-ids i-0abcdef1234567890
```

## 執行個體生命週期

執行個體有以下幾種狀態：pending（啟動中）、running（執行中）、stopping（停止中）、stopped（已停止）、terminated（已終止）。停止的執行個體不會收 CPU 費用，但 EBS 儲存仍需收費。終止後執行個體會消失，所有資料無法恢復。

## 參考資源

- https://www.google.com/search?q=AWS+EC2+執行個體+啟動+Security+Group+SSH+連線+設定+2016
- https://www.google.com/search?q=AWS+CLI+ec2+run-instances+describe-instances+操作+範例
- https://www.google.com/search?q=EC2+執行個體+生命週期+stop+terminate+差異+費用