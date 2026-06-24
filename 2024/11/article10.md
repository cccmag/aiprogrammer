# Terraform 入門

## 1. 引言

Terraform 是 HashiCorp 開發的基礎設施即程式碼（IaC）工具。它使用宣告式配置語言 HCL（HashiCorp Configuration Language）來定義和管理雲端基礎設施。本文將從零開始介紹 Terraform 的核心概念與實戰應用。

## 2. 安裝與初始化

```bash
# macOS 安裝
brew install terraform

# 驗證安裝
terraform version

# 建立專案目錄
mkdir my-infra && cd my-infra
```

## 3. Provider 配置

Provider 是 Terraform 與雲端服務商溝通的橋樑：

```hcl
# main.tf
terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = "us-west-2"
}
```

## 4. 資源定義

```hcl
# 建立 VPC
resource "aws_vpc" "main" {
  cidr_block = "10.0.0.0/16"
  tags = {
    Name = "production"
  }
}

# 建立子網
resource "aws_subnet" "public" {
  vpc_id            = aws_vpc.main.id
  cidr_block        = "10.0.1.0/24"
  availability_zone = "us-west-2a"
}

# 建立安全群組
resource "aws_security_group" "web" {
  name   = "web-sg"
  vpc_id = aws_vpc.main.id

  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

# 建立 EC2 實例
resource "aws_instance" "web" {
  ami                    = "ami-0c55b159cbfafe1f0"
  instance_type          = "t2.micro"
  subnet_id              = aws_subnet.public.id
  vpc_security_group_ids = [aws_security_group.web.id]

  user_data = <<-EOF
    #!/bin/bash
    apt-get update
    apt-get install -y nginx
    systemctl start nginx
  EOF

  tags = {
    Name = "web-server"
  }
}
```

## 5. 變數與輸出

```hcl
# variables.tf
variable "instance_type" {
  description = "EC2 instance type"
  type        = string
  default     = "t2.micro"
}

variable "environment" {
  description = "Environment name"
  type        = string
}

# outputs.tf
output "instance_ip" {
  description = "Public IP of web server"
  value       = aws_instance.web.public_ip
}

output "vpc_id" {
  value = aws_vpc.main.id
}
```

## 6. 狀態管理

Terraform 使用狀態檔案追蹤基礎設施的當前狀態：

```bash
# 遠端狀態儲存（S3 + DynamoDB）
terraform {
  backend "s3" {
    bucket         = "my-terraform-state"
    key            = "production/terraform.tfstate"
    region         = "us-west-2"
    dynamodb_table = "terraform-locks"
    encrypt        = true
  }
}
```

## 7. 常用命令

```bash
# 初始化專案
terraform init

# 格式化配置檔案
terraform fmt

# 驗證配置語法
terraform validate

# 預覽變更
terraform plan

# 套用變更
terraform apply -auto-approve

# 銷毀資源
terraform destroy
```

## 8. 結語

Terraform 讓基礎設施管理變得像管理程式碼一樣簡單。通過宣告式配置、版本控制和自動化部署，團隊可以實現基礎設施的完全自動化。建議從小型專案開始，逐步擴展到完整的基礎設施管理。
