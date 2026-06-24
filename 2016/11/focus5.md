# Infrastructure as Code（2012-2016）

## 前言

Infrastructure as Code（IaC）用程式碼管理基礎設施，讓基礎設施的建置、修改都能追蹤版本、可重複執行。

## IaC 核心原則

1. **版本控制**：所有基礎設施定義在 Git 中
2. **可重複**：相同的程式碼產生相同的環境
3. **自動化**：減少人為操作錯誤
4. **文件化**：程式碼即文件

## Terraform 基本語法

### Provider 設定

```hcl
# providers.tf
provider "aws" {
  region = "ap-northeast-1"
  profile = "default"
}

provider "aws" {
  alias  = "uswest"
  region = "us-west-2"
}
```

### 資源定義

```hcl
# main.tf

resource "aws_vpc" "main" {
  cidr_block           = "10.0.0.0/16"
  enable_dns_hostnames = true
  enable_dns_support   = true
  
  tags {
    Name        = "main-vpc"
    Environment = "production"
  }
}

resource "aws_subnet" "public" {
  vpc_id                  = "${aws_vpc.main.id}"
  cidr_block              = "10.0.1.0/24"
  availability_zone       = "ap-northeast-1a"
  map_public_ip_on_launch = true
  
  tags {
    Name = "public-subnet"
  }
}

resource "aws_subnet" "private" {
  vpc_id            = "${aws_vpc.main.id}"
  cidr_block        = "10.0.2.0/24"
  availability_zone = "ap-northeast-1a"
  
  tags {
    Name = "private-subnet"
  }
}
```

### 資料來源

```hcl
data "aws_ami" "ubuntu" {
  most_recent = true
  owners      = ["099720109477"]  # Canonical
  
  filter {
    name   = "name"
    values = ["ubuntu/images/hvm-ssd/ubuntu-xenial-16.04-amd64-server-*"]
  }
}
```

### 輸出變數

```hcl
# outputs.tf
output "vpc_id" {
  value = "${aws_vpc.main.id}"
}

output "public_subnet_ids" {
  value = "${aws_subnet.public.*.id}"
}

output "private_subnet_ids" {
  value = "${aws_subnet.private.*.id}"
}
```

## Ansible 基本語法

### Playbook

```yaml
# playbook.yml
---
- hosts: webservers
  become: yes
  vars:
    node_version: "6"
    
  tasks:
    - name: Install Node.js
      apt:
        name: nodejs
        state: present
      when: ansible_os_family == "Debian"
    
    - name: Install npm
      apt:
        name: npm
        state: present
      
    - name: Copy application files
      git:
        repo: https://github.com/org/myapp.git
        dest: /var/www/myapp
        force: yes
        
    - name: Install dependencies
      npm:
        path: /var/www/myapp
        
    - name: Start application
      systemd:
        name: myapp
        state: started
        enabled: yes
```

### Roles 結構

```
roles/
├── common/
│   ├── tasks/
│   │   └── main.yml
│   ├── handlers/
│   │   └── main.yml
│   └── templates/
│       └── ntp.conf.j2
├── nginx/
│   ├── tasks/
│   │   └── main.yml
│   └── templates/
│       └── nginx.conf.j2
└── myapp/
    ├── tasks/
    │   └── main.yml
    └── handlers/
        └── main.yml
```

### Inventory

```ini
# hosts.ini
[webservers]
web1.example.com ansible_host=192.168.1.10
web2.example.com ansible_host=192.168.1.11

[databases]
db1.example.com ansible_host=192.168.1.20

[webservers:vars]
ansible_user=deploy
ansible_python_interpreter=/usr/bin/python3
```

## 基礎設施測試

### Terratest（Go）

```go
package test

import (
    "testing"
    "github.com/gruntwork-io/terratest/modules/terraform"
    "github.com/stretchr/testify/assert"
)

func TestTerraformExample(t *testing.T) {
    terraformOptions := &terraform.Options{
        TerraformDir: "../examples/terraform-example",
        Vars: map[string]interface{}{
            "environment": "test",
        },
    }
    
    defer terraform.Destroy(t, terraformOptions)
    terraform.InitAndApply(t, terraformOptions)
    
    instanceID := terraform.Output(t, terraformOptions, "instance_id")
    assert.NotEmpty(t, instanceID)
}
```

### Ansible Molecule

```yaml
# molecule.yml
molecule:
  name: myrole
  driver:
    name: docker
  lint:
    name: yamllint
  platforms:
    - name: instance
      image: ubuntu:16.04
  provisioner:
    name: ansible
    lint:
      name: ansible-lint
  verifier:
    name: testinfra
    lint:
      name: flake8
```

## 延伸閱讀

- [Terraform 官方文檔](https://www.google.com/search?q=terraform+tutorial+2016)
- [Ansible 入門](https://www.google.com/search?q=ansible+tutorial+2016)
- [Infrastructure as Code 實踐](https://www.google.com/search?q=infrastructure+as+code+best+practices+2016)

## 結語

IaC 讓基礎設施管理變得跟程式碼一樣——可版本控制、可測試、可審查。這是 DevOps 的重要支柱。

---

*本篇文章為「AI 程式人雜誌 2016 年 11 月號」DevOps 系列之一。*