# 推薦系統的原理與實踐

## 協同過濾

```javascript
function recommend(userId, itemId) {
    var similarUsers = findSimilarUsers(userId);
    var predictions = aggregateRatings(similarUsers, itemId);
    return predictions;
}
```

## 應用

- 電子商務
- 影音平台
- 社交網路

## 結論

推薦系統提升使用者體驗。

---

**延伸閱讀**

- [Recommendation+system+tutorial](https://www.google.com/search?q=recommendation+system+tutorial)