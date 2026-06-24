# VPC 網路架構

## VPC 基礎

Amazon VPC（Virtual Private Cloud）讓你在 AWS 中建立隔離的虛擬網路環境。你可完全控制 IP 範圍、子網路、路由表、閘道等網路元件。預設情況下，每個新帳戶都會有一個「Default VPC」，但自訂 VPC 能提供更精細的控制。

## 建立 VPC

```bash
# 建立 VPC，指定 IPv4 CIDR 區塊
aws ec2 create-vpc --cidr-block 10.0.0.0/16

# 啟用 DNS 主機名稱
aws ec2 modify-vpc-attribute --vpc-id vpc-12345678 --enable-dns-hostnames "{\"Value\":true}"
```

## 子網路規劃

建議將 VPC 劃分為公有子網路（可訪問網際網路）與私有子網路（僅內部訪問）。

```
VPC: 10.0.0.0/16
  |
  +--公有子網路 A: 10.0.1.0/24 (可用區域 AZ1)
  |    用途：NAT 閘道、負載平衡器
  |
  +--公有子網路 B: 10.0.2.0/24 (可用區域 AZ2)
  |
  +--私有子網路 C: 10.0.10.0/24 (AZ1)
  |    用途：應用伺服器、資料庫
  |
  +--私有子網路 D: 10.0.20.0/24 (AZ2)
```

## 網路 ACL 與 Security Group

**Security Group**：具狀態的防火牆，綁定到 EC2 執行個體。允許規則的流量自動允許回傳。

**Network ACL**：無狀態的防火牆，綁定到子網路層級。所有流量都需明確允許。

## 網際網路閘道與 NAT

公有子網路中的執行個體需要「網際網路閘道（Internet Gateway）」才能訪問外部網路。

```bash
# 建立網際網路閘道
aws ec2 create-internet-gateway

# 附加到 VPC
aws ec2 attach-internet-gateway --internet-gateway-id igw-12345678 --vpc-id vpc-12345678

# 建立路由表並加入網際網路路由
aws ec2 create-route-table --vpc-id vpc-12345678
aws ec2 create-route --route-table-id rtb-12345678 --destination-cidr-block 0.0.0.0/0 --gateway-id igw-12345678
```

私有子網路透過 NAT 閘道或 NAT 執行個體訪問外部網路，不能直接被外部訪問，增加安全性。

## VPC 對等連線

VPC 對等連線允許兩個 VPC 之間進行私有 IP 通訊，無需透過網際網路或 VPN。

```bash
# 建立 VPC 對等連線請求
aws ec2 create-vpc-peering-connection --vpc-id vpc-12345678 --peer-vpc-id vpc-87654321

# 接受連線請求（在被請求端執行）
aws ec2 accept-vpc-peering-connection --vpc-peering-connection-id pcx-12345678
```

## 參考資源

- https://www.google.com/search?q=AWS+VPC+建立+子網路+公有+私有+路由表+設定+2016
- https://www.google.com/search?q=VPC+網際網路閘道+NAT+Security+Group+網路ACL+差異
- https://www.google.com/search?q=VPC+對等連線+Peering+多VPC+網路架構+規劃