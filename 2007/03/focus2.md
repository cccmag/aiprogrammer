# PHP 的繁榮：Web 開發的主流選擇

## 前言

2007 年，PHP 是世界上最流行的 Web 開發語言，估計有 70% 的網站使用 PHP。

## PHP 的生態系

### 重要里程碑

```
┌────────────────────────────────────────────────────────┐
│              PHP 發展時間線                             │
├────────────────────────────────────────────────────────┤
│                                                        │
│  1995：PHP/FI 發布                                    │
│  1998：PHP 3.0                                        │
│  2000：PHP 4.0                                        │
│  2004：PHP 5.0（ Zend Engine II ）                    │
│  2006：PHP 5.2                                        │
│                                                        │
│  2007 年：市場佔有率約 70%                            │
│                                                        │
└────────────────────────────────────────────────────────┘
```

## PHP 5 的物件導向

```php
<?php
// PHP 5 物件導向
class User {
    private $name;
    private $email;

    public function __construct($name, $email) {
        $this->name = $name;
        $this->email = $email;
    }

    public function getName() {
        return $this->name;
    }
}

$user = new User("John", "john@example.com");
echo $user->getName();
?>
```

## WordPress 現象

WordPress 的成功代表了 PHP 生態系的繁榮：

```python
# WordPress 統計（2007 年）
WORDPRESS_2007 = {
    "市場佔有率": "~10% of all websites",
    "外掛數量": "1000+",
    "主題數量": "500+"
}
```

## 結論

PHP 的簡單性、廣泛的宿主支援和豐富的函式庫，使其在 2007 年繼續統治 Web 開發領域。

---

*本篇文章為「AI 程式人雜誌 2007 年 3 月號」本期焦點系列文章。*