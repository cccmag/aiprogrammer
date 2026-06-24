# 推薦系統的協同過濾技術

## 協同過濾

### User-based CF

```python
# 找相似用戶
similar_users = find_similar_users(target_user)
predictions = aggregate_ratings(similar_users)
```

### Item-based CF

```python
# 找相似物品
similar_items = find_similar_items(target_item)
predictions = aggregate_ratings_for_item(similar_items)
```

## 應用

- Netflix 電影推薦
- Amazon 商品推薦

## 結論

協同過濾是推薦系統的核心技術。

---

**延伸閱讀**

- [Collaborative+filtering+tutorial](https://www.google.com/search?q=collaborative+filtering+tutorial)