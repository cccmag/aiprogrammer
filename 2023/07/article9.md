# X.509 憑證鏈

## 數位世界的信任

在現實世界中，我們使用護照、駕照和身分證來證明身分。這些文件由權威機構（政府）簽發，具有法律效力。在數位世界中，X.509 憑證和公開金鑰基礎設施（PKI）扮演著類似的角色。

## X.509 v3 憑證格式

X.509 憑證是將公鑰與持證人身分綁定的數位文件。v3 版本（1988 年引入）是目前最常用的版本。

### 基本欄位

```
Certificate:
    Version: 3
    Serial Number: 0x...
    Signature Algorithm: sha256WithRSAEncryption
    Issuer: CN=Example Root CA
    Validity:
        Not Before: Jan 1 00:00:00 2023
        Not After : Jan 1 00:00:00 2028
    Subject: CN=example.com
    Subject Public Key Info:
        Public Key Algorithm: rsaEncryption
        RSA Public-Key: (2048 bit)
    Extensions:
        ...
    Signature Algorithm: sha256WithRSAEncryption
    Signature: ...
```

### v3 延伸欄位

X.509 v3 引入的延伸欄位使憑證更加靈活：

- **Basic Constraints**：標記是否為 CA 憑證
- **Key Usage**：指定金鑰用途（數位簽章、金鑰加密等）
- **Extended Key Usage**：指定擴展用途（TLS 伺服器認證、程式碼簽章等）
- **Subject Alternative Name (SAN)**：指定其他主體名稱（域名、IP 等）
- **CRL Distribution Points**：憑證撤銷列表的下載位置
- **Authority Information Access**：CA 資訊和 OCSP 回應器地址

## 憑證鏈的建立

憑證鏈（Certificate Chain）是信任傳遞的機制。典型的鏈結構：

```
Root CA (自簽名)
  └─ Intermediate CA 1
       └─ Intermediate CA 2
            └─ 終端實體憑證 (leaf/end-entity)
```

### 根 CA

根 CA（Root CA）是信任錨點（Trust Anchor）。其憑證是自簽名的——CA 用自己的私鑰簽署自己的憑證。根 CA 憑證通過作業系統或瀏覽器內建的信任商店（Trust Store）分發。

根 CA 的安全極為重要。如果根 CA 私鑰洩露，整個信任鏈都將崩潰。因此根 CA 通常離線儲存，在高度安全的環境中操作。

### 中間 CA

中間 CA（Intermediate CA）由根 CA 或其他中間 CA 簽名。使用中間 CA 的好處是：

- 根 CA 可以離線保存，減少暴露風險
- 可以為不同用途簽發不同中間 CA
- 如果中間 CA 被攻擊，可以只撤銷該中間 CA 而不影響根 CA

## 憑證驗證流程

當客戶端驗證伺服器憑證時：

1. 從伺服器接收終端憑證和中間 CA 憑證
2. 驗證每個憑證的簽章（從終端向上到根 CA）
3. 檢查每個憑證的有效期
4. 檢查憑證是否被撤銷（CRL 或 OCSP）
5. 驗證憑證的 Key Usage 和 EKU
6. 檢查域名是否匹配 SAN
7. 確認根 CA 在信任商店中

## 憑證撤銷

憑證可能因為私鑰洩露、離職或其他原因在到期前被撤銷。有兩種主要撤銷機制：

### CRL（Certificate Revocation List）

CA 定期發布撤銷憑證的列表。瀏覽器下載 CRL 並檢查目標憑證是否在列表中。CRL 的缺點是延遲——從撤銷到發布可能間隔數天。

### OCSP（Online Certificate Status Protocol）

OCSP 允許即時查詢憑證狀態。客戶端發送查詢請求到 OCSP 回應器，獲得「良好」、「撤銷」或「未知」的回應。OCSP 裝訂（OCSP Stapling）讓伺服器提供已簽名的 OCSP 回應，提高隱私性並減少延遲。

## 延伸閱讀

- [X.509 標準](https://www.google.com/search?q=X.509+certificate+standard+ITU)
- [PKI 基礎](https://www.google.com/search?q=public+key+infrastructure+PKI)
- [Let's Encrypt 憑證鏈](https://www.google.com/search?q=Let%27s+Encrypt+certificate+chain)
- [OCSP vs CRL](https://www.google.com/search?q=OCSP+vs+CRL+certificate+revocation)
- [Certificate Transparency](https://www.google.com/search?q=certificate+transparency+log)

---

*本篇文章為「AI 程式人雜誌 2023 年 7 月號」精選文章。*
