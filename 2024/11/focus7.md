# 基礎設施即程式碼

## IaC 宣言與 Terraform

### 前言

基礎設施即程式碼（Infrastructure as Code, IaC）是 DevOps 的關鍵實踐之一。它將伺服器、網路、資料庫等基礎設施的配置以程式碼的形式管理，確保環境的可重複性和版本控制。本節將探討 IaC 的核心概念與 Terraform 的實戰應用。

### 為什麼需要 IaC

傳統的基礎設施管理依賴手動操作和「寵物伺服器」模式——伺服器像寵物一樣有名字，出問題時手動修復。IaC 倡導「牲畜伺服器」模式——伺服器可隨時替換，出問題時直接重建。

**IaC 的優勢**：
- 可重複性：每次部署環境一致
- 版本控制：基礎設施變更有完整歷史
- 自動化：減少人為錯誤
- 文件化：程式碼即文件

### 聲明式 vs 命令式

IaC 工具分為兩大類：

**命令式（Imperative）**：描述如何達到目標狀態

```bash
# 命令式：一步步操作
apt-get install nginx
systemctl enable nginx
ufw allow 80/tcp
```

**聲明式（Declarative）**：描述目標狀態是什麼

```hcl
# 聲明式：描述想要的結果
resource "aws_instance" "web" {
  ami           = "ami-0c55b159cbfafe1f0"
  instance_type = "t2.micro"
  tags = {
    Name = "web-server"
  }
}
```

Terraform 採用聲明式方式，工具會自動計算如何達到目標狀態。

### Terraform 核心概念

**Provider**：與雲端服務商互動的外掛

```hcl
terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}
```

**Resource**：基礎設施元件

```hcl
resource "aws_security_group" "web" {
  name = "web-sg"

  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
}
```

**State**：狀態檔案，記錄當前基礎設施狀態

```bash
# 初始化 Terraform
terraform init

# 預覽變更
terraform plan

# 套用變更
terraform apply

# 銷毀資源
terraform destroy
```

### 模組化設計

使用模組封裝可重複使用的基礎設施元件：

```hcl
module "vpc" {
  source   = "./modules/vpc"
  cidr     = "10.0.0.0/16"
  name     = "production"
}

module "ecs_cluster" {
  source    = "./modules/ecs"
  vpc_id    = module.vpc.id
  subnet_ids = module.vpc.public_subnets
}
```

### CI/CD 與 IaC 的整合

在 CI/CD 管線中自動執行 Terraform：

```yaml
jobs:
  terraform:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: hashicorp/setup-terraform@v3
      - run: terraform init
      - run: terraform fmt -check
      - run: terraform plan
      - run: terraform apply -auto-approve
```

### 小結

IaC 是 DevOps 自動化部署的頂層實踐。通過 Terraform 等工具，團隊可以用程式碼管理完整的基礎設施生命週期，實現真正的一鍵部署與環境一致性。

---

**下一步**：[文章集錦](articles.md)

## 延伸閱讀

- [Terraform 入門指南](https://www.google.com/search?q=Terraform+getting+started+guide)
- [IaC 最佳實踐](https://www.google.com/search?q=Infrastructure+as+Code+best+practices)
