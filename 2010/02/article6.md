# Google 收購 Aardvark：社群搜尋

## 收購概述

### 交易詳情

2010 年 2 月，Google 收購了 Aardvark，這是一家專注於社群問答搜尋的新創公司。

```
Google-Aardvark 收購案：
───────────────────────────
收購時間：     2010 年 2 月
金額：         未公開（據估約 $5000 萬）
目的：         強化社群搜尋能力
團隊：         併入 Google
```

## Aardvark 介紹

### 公司背景

```
Aardvark 歷史：
───────────────────────────
成立：        2007 年
創辦人：      Dustin R. Ward、Vaughan P. Ehrich
天使輪：      ~$100 萬
A 輪：        $1100 萬（True Ventures）
被收購：      2010 年 2 月
```

### 服務特色

```
Aardvark 核心功能：
───────────────────────────
社群問答：     透過社群網路回答問題
智慧匹配：     將問題導給適合回答的人
Social Graph： 利用社交網路找到專家
即時通知：     Email、IM 通知回答
```

## 技術架構

### 運作原理

```
Aardvark 工作流程：
───────────────────────────
1. 使用者提出問題
2. 系統分析問題內容
3. 根據 Social Graph 找到可能知道答案的人
4. 邀請匹配的人回答
5. 收集回答並傳給提問者
6. 根據品質評分排序答案
```

### 智慧匹配演算法

```python
# 簡化的匹配邏輯
def match_question_to_users(question, users, social_graph):
    # 分析問題關鍵字
    keywords = extract_keywords(question)

    # 計算每位用戶的匹配分數
    scored_users = []
    for user in users:
        score = 0
        score += keyword_match(user.expertise, keywords)
        score += social_distance(social_graph, question.asker, user)
        score += response_rate(user) * 0.5
        scored_users.append((user, score))

    # 返回最高分用戶
    scored_users.sort(key=lambda x: x[1], reverse=True)
    return [user for user, score in scored_users[:5]]
```

## 人工智慧應用

### 自然語言處理

```
Aardvark 的 NLP 技術：
───────────────────────────
問題分類：     主題識別
實體抽取：     人名、地點、組織
關鍵字提取：   主題詞彙
相似問題：     找相關問題
```

### 社群網路分析

```
Social Graph 分析：
───────────────────────────
網路強度：     互動頻率
共同興趣：     主題重疊度
專業領域：     過去的回答品質
響應速度：     回覆時間
上線時間：     可及時回覆
```

## 對 Google 的價值

### 搜尋戰略

```
收購動機：
───────────────────────────
強化社群搜尋：  回答難以網頁內容回答的問題
專家網路：     利用專家回答品質問題
Social Search： 結合社交與搜尋
使用者參與：   提高使用者黏著度
```

### 技術整合

```
可能的整合方向（2010 年）：
───────────────────────────
Google Search：  結果頁面顯示社群答案
Gmail：         整合問答功能
Google Profile： 建立專家檔案
Google Alerts：  主題通知
```

## 隱私考量

### 資料使用

```
隱私疑慮：
───────────────────────────
資料收集：     使用者的社交關係和回答
存取權限：     需要存取社交網路
通知：         透過 Email/IM 發送
商業使用：     Google 的資料政策
```

### 使用者控制

```
Aardvark 的隱私控制：
───────────────────────────
選擇性參與：    可選擇不回答問題
問題過濾：     可設定不接收特定主題
社交網路：     控制存取哪些社交資料
刪除：         可刪除帳戶和資料
```

---

## 結論

Google 收購 Aardvark 顯示了社群搜尋的重要性。透過結合人工智慧和社交網路，Aardvark 提供了解決「找不到答案」的問題的新方式。

這個收購反映了搜尋引擎未來的方向：不只是索引網頁內容，而是連結需要答案的人和能夠提供答案的人。

---

*本期文章到此結束。*