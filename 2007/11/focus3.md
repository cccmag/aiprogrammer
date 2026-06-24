# OpenSocial 標準：Google 的回應

## OpenSocial 的起源

2007 年 11 月，Google 發布了 OpenSocial 規範，作為對 Facebook 封閉生態系統的回應。

### OpenSocial 的目標

```
OpenSocial 的目標：
───────────────────
1. 開放標準
2. 跨平台相容
3. 多社交網路支援
```

### 支持者

```python
# OpenSocial 支持者
# - MySpace
# - Orkut
# - LinkedIn
# - Salesforce
# - Friendster
# - Hi5
```

## OpenSocial API

### 核心 API

```javascript
// OpenSocial 應用程式範例
gadgets.util.registerOnLoadHandler(function() {
    // 取得當前用戶
    opensocial.newDataRequest().newFetchPersonRequest('OWNER', function(response) {
        var data = response.getData();
        var name = data.getDisplayName();
        document.getElementById('name').innerHTML = 'Hello, ' + name;
    });
});
```

### 社交圖譜 API

```javascript
// 取得好友列表
var req = opensocial.newDataRequest();
req.add(req.newFetchPeopleRequest('OWNER_FRIENDS'), 'friends');

req.send(function(response) {
    var friends = response.get('friends').getData();
    friends.each(function(person) {
        console.log(person.getDisplayName());
    });
});
```

### Activity API

```javascript
// 發布活動
var activity = opensocial.newActivity({
    title: 'Just played FarmVille!',
    url: 'http://farmville.com/achievement/123'
});

opensocial.requestActivity(
    activity,
    function(response) {
        if (response.hadError()) {
            console.error('Error posting activity');
        }
    }
);
```

## 與 Facebook API 的比較

```
OpenSocial vs Facebook API：
────────────────────────────────────────────────────────
特性              OpenSocial           Facebook API
────────────────────────────────────────────────────────
語言              JavaScript (Gadget)   FBML/PHP/Python
社交圖譜          統一 API             專有 API
多平台支援        ✓                    ✗
覆蓋範圍          多個社交網路         僅 Facebook
成熟度            新（2007）           已有數月
────────────────────────────────────────────────────────
```

## 結語

OpenSocial 雖然最終沒有取代 Facebook API，但它推動了社交應用的開放標準運動。

---

## 延伸閱讀

- [OpenSocial+2007+Google](https://www.google.com/search?q=OpenSocial+2007+Google)

---