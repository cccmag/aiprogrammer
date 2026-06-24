# 申請 AWS 免費帳戶

## 註冊流程

AWS 免費帳戶是學習雲端的最佳起點，註冊過程免費，無需一開始就提供信用卡資訊（不同的地區可能有不同的政策）。

1. 前往 AWS 官網點選「建立 AWS 帳戶」
2. 輸入電子郵件地址與密碼作為登入憑據
3. 選擇「個人」帳戶類型，填寫姓名、地址、電話號碼
4. 驗證電子郵件地址（AWS 會傳送驗證碼）
5. 填寫信用卡資訊（即使有免費方案，部分服務仍可能收費）
6. 完成身份驗證，可能需要拍攝證件照片上傳

## 雙重驗證設定

註冊完成後，第一件應該做的事是啟用雙重驗證（Multi-Factor Authentication, MFA）。AWS 支援虛擬 MFA 應用程式（如 Google Authenticator）與硬體 MFA 裝置。

設定步驟：
1. 登入 AWS Console，進入「我的安全性憑證」頁面
2. 選擇「啟用 MFA」並選擇硬體或虛擬 MFA 裝置
3. 若選擇虛擬 MFA，開啟驗證器應用程式，掃描 QR Code
4. 輸入驗證器顯示的兩組連續驗證碼完成設定

## 推薦的安全設定

**建立 IAM 使用者而非使用 Root 帳戶**：Root 帳戶擁有完全控制權，一旦被入侵後果嚴重。建立 IAM 使用者並赋予最小必要權限，日常操作一律使用 IAM。

**啟用 CloudTrail**：CloudTrail 會記錄所有 AWS API 呼叫，是安全審計與事件調查的基礎。預設免費方案就包含部分 CloudTrail 功能。

**設定 billing警示**：進入「我的帳戶」→「預算」，設定帳單花費警示。當月費超過設定金額時，AWS 會發送電子郵件通知。

## 免費方案說明

AWS 免費方案分為三類：

**永遠免費**：部分服務終生免費，如 AWS Lambda 每月 100 萬個請求、S3 5GB 儲存、T2 與 T3 微實例等。

**12 個月免費**：新帳戶首年適用的優惠，如 EC2 t2.micro 每月 750 小時、S3 30GB 儲存等。

**短期試用**：部分服務提供的限時試用，如 Amazon DynamoDB 25GB 儲存等。

## 參考資源

- https://www.google.com/search?q=AWS+免費帳戶+申請+註冊+流程+雙重驗證+MFA+2016
- https://www.google.com/search?q=AWS+IAM+使用者+權限+安全+Best+Practices+設定
- https://www.google.com/search?q=AWS+CloudTrail+billing+警示+安全+審計+設定