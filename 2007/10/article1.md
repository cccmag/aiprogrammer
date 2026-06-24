# Amazon EC2 詳解：彈性運算雲

## 前言

2007 年的 Amazon EC2 提供了雲端運算的核心能力——彈性、可擴展的虛擬機器。

## EC2 核心概念

```python
# EC2 使用 boto
import boto.ec2

conn = boto.ec2.connect_to_region('us-east-1')
reservation = conn.run_instances(
    'ami-12345',
    instance_type='m1.small'
)
```

## 結語

EC2 開創了 IaaS 的時代。

---

## 延伸閱讀

- [Amazon+EC2+2007](https://www.google.com/search?q=Amazon+EC2+2007)

---