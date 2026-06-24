# IAM 權限管理

## IAM 基本概念

IAM（Identity and Access Management）是 AWS 的身份識別與存取管理服務，用於控制「誰」可以「對哪些資源」執行「什麼操作」。良好的 IAM 設定是雲端安全的基石。

## IAM 重要術語

**使用者（User）**：需要登入 AWS Console 或程式中存取 AWS 資源的人員或應用程式。

**群組（Group）**：將多個使用者歸類，套用相同權限。適用於依部門或角色管理權限。

**角色（Role）**：賦予 AWS 服務或外部人員臨時存取資源的權限。適合跨帳戶存取或服務間授權。

**政策（Policy）**：定義許可權的 JSON 文件，可附加到使用者、群組或角色。

## 建立 IAM 使用者

```bash
# 建立使用者
aws iam create-user --user-name developer

# 建立存取金鑰（用於 CLI/SDK）
aws iam create-access-key --user-name developer

# 將使用者加入群組
aws iam add-user-to-group --user-name developer --group-name developers
```

## 最小權限原則

安全最佳實踐是「最小權限原則」—— 只授予完成工作所需的最小權限，而非管理員完全存取。

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "s3:GetObject",
                "s3:PutObject"
            ],
            "Resource": "arn:aws:s3:::my-app-bucket/*"
        }
    ]
}
```

## 角色設定

將角色附加到 EC2 執行個體，讓執行個體中的應用程式以該角色身份執行，而非使用硬編碼的 access key。

```bash
# 建立角色
aws iam create-role --role-name MyEC2Role --assume-role-policy-document file://trust-policy.json

# 附加政策
aws iam attach-role-policy --role-name MyEC2Role --policy-arn arn:aws:iam::aws:policy/AmazonS3ReadOnlyAccess

# 將角色附加到 EC2 執行個體（在建立執行個體時指定）
aws ec2 run-instances ... --iam-instance-profile Name=MyEC2Role
```

## MFA 重要提醒

對具有管理員權限的 IAM 使用者，強烈建議啟用 MFA（多因素認證）。萬一密碼洩漏，攻擊者仍無法登入。

## 參考資源

- https://www.google.com/search?q=AWS+IAM+使用者+群組+角色+政策+權限+管理+設定+2016
- https://www.google.com/search?q=IAM+最小權限原則+Policy+JSON+最佳實踐+安全
- https://www.google.com/search?q=IAM+Role+EC2+執行個體+臨時憑證+安全+Best+Practices