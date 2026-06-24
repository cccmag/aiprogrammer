# 社交網路的崛起：從 Friendster 到 Facebook

## 社交網路的起源

### 早期社交網路

```
社交網路演化：
───────────────
1997  SixDegrees.com    第一個社交網路
1998  Friendster        病毒式傳播
2002  Orkut             Google 收購
2003  MySpace           音樂和青少年市場
2004  Facebook         大學生市場
2006  Twitter           微網誌
2007  OpenSocial        開放標準
```

## SixDegrees（1997）

第一個規模化的社交網路服務。

```python
# SixDegrees 的核心概念
class User:
    friends = []  # 好友列表
    profile = {}   # 個人資料

    def add_friend(self, user):
        self.friends.append(user)

    def get_friends_of_friends(self):
        # 三度分隔理論
        fof = set()
        for friend in self.friends:
            for fof_friend in friend.friends:
                if fof_friend != self:
                    fof.add(fof_friend)
        return fof
```

## Friendster（2002）

Friendster 首先達到百萬用戶，但後來被 MySpace 超越。

```python
# Friendster 的影響
# 1. 驗證了社交網路的商業模式
# 2. 引入了「六度分隔」概念
# 3. 開創了虛擬禮物等營收模式
```

## MySpace（2003）

MySpace 成為主流社交網路，特別是在音樂產業。

```python
# MySpace 的特點
# 1. 可自訂頁面設計
# 2. 音樂嵌入
# 3. 青少年市場主導
# 4. 病毒式推廣
```

## Facebook（2004）

### Facebook 的起源

```python
# Facebook 起源
# 2004 年，Mark Zuckerberg 在哈佛大學建立
# 最初只對哈佛學生開放
# 後來擴展到其他大學
# 2006 年對所有人開放
```

### Facebook 的創新

```
Facebook 的創新：
──────────────────
1. 動態消息（News Feed）
2. 開放平台
3. 社交遊戲
4. 粉絲專頁
5. 事件功能
```

### Facebook 的技術架構

```python
# Facebook 早期架構（2007 年）
# - PHP（後來用 HHVM）
# - MySQL
# - Memcached
# - 自行開發的 HipHop PHP 編譯器
```

## 結語

從 SixDegrees 到 Facebook，社交網路經歷了十年的演進。每代產品都在解決前代的問題，同時創造新的可能性。

---

## 延伸閱讀

- [social+network+history+2007](https://www.google.com/search?q=social+network+history+2007)

---