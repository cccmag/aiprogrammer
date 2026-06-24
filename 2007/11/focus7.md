# 社交網路的商業模式

## 社交網路營收來源

### 1. 廣告收入

```python
# 社交網路廣告系統
class AdSystem:
    def __init__(self):
        self.campaigns = []

    def target_ads(self, user, ad_content):
        # 根據使用者資料進行廣告定向
        targeting_data = {
            'age': user.get('age'),
            'location': user.get('location'),
            'interests': user.get('interests'),
            'friends': user.get('friends')
        }
        return self._match_ads(ad_content, targeting_data)

    def _match_ads(self, ad, targeting):
        # 匹配演算法
        score = 0
        if ad.target_age == targeting['age']:
            score += 1
        if ad.target_location == targeting['location']:
            score += 1
        return score
```

### 2. 虛擬商品

```python
# 虛擬商品系統
class VirtualGoods:
    def __init__(self):
        self.inventory = {}
        self.prices = {
            'gift': 1.00,
            'avatar_item': 2.50,
            'game_currency': 0.01
        }

    def purchase(self, user_id, item_id):
        # 購買虛擬商品
        if user_id in self.inventory:
            self.inventory[user_id].append(item_id)
        else:
            self.inventory[user_id] = [item_id]
        return True

    def gift(self, from_user, to_user, item_id):
        # 贈送虛擬禮物
        pass
```

### 3. 付費訂閱

```python
# 付費訂閱模式
class Subscription:
    def __init__(self):
        self.plans = {
            'basic': 0,
            'premium': 4.99,
            'gold': 9.99
        }

    def upgrade(self, user_id, plan):
        if plan in self.plans:
            return {
                'user_id': user_id,
                'plan': plan,
                'price': self.plans[plan],
                'features': self._get_features(plan)
            }
        return None

    def _get_features(self, plan):
        features = {
            'basic': ['基本功能'],
            'premium': ['基本功能', '無廣告', '更多儲存空間'],
            'gold': ['基本功能', '無廣告', '無限儲存', '優先支援']
        }
        return features.get(plan, [])
```

### 4. 平台佣金

```python
# 應用程式平台佣金
class PlatformCommission:
    def __init__(self):
        self.commission_rate = 0.30  # Facebook 收取 30%

    def calculate_revenue(self, app_revenue):
        platform_cut = app_revenue * self.commission_rate
        developer_cut = app_revenue - platform_cut
        return {
            'platform': platform_cut,
            'developer': developer_cut
        }
```

## 使用者資料貨幣化

```bash
# 資料價值的層次
# Level 1: 匿名統計 - 趨勢分析
# Level 2: 定向廣告 - 提升廣告效果
# Level 3: 個人化推薦 - 電子商務
# Level 4: 資料銷售 - 研究機構
```

## 結語

社交網路的商業模式正在持續演化。從廣告到虛擬商品，每種模式都有其獨特的價值創造方式。

---

## 延伸閱讀

- [social+network+business+model+2007](https://www.google.com/search?q=social+network+business+model+2007)

---