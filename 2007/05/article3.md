# RSS 2.0 與 Atom：資訊聚合標準

## 前言

RSS 和 Atom 是 2007 年部落格和新聞聚合的標準格式。

## RSS 2.0 範例

```xml
<rss version="2.0">
  <channel>
    <title>My Blog</title>
    <link>http://example.com</link>
    <item>
      <title>New Post</title>
      <link>http://example.com/post1</link>
      <pubDate>Tue, 15 May 2007 10:00:00 GMT</pubDate>
    </item>
  </channel>
</rss>
```

## Atom 範例

```xml
<feed xmlns="http://www.w3.org/2005/Atom">
  <title>My Blog</title>
  <entry>
    <title>New Post</title>
    <link href="http://example.com/post1"/>
    <updated>2007-05-15T10:00:00Z</updated>
  </entry>
</feed>
```

## 結語

Atom 相比 RSS 提供了更好的標準化和擴展性。

---

## 延伸閱讀

- [RSS+2.0+vs+Atom+specification](https://www.google.com/search?q=RSS+2.0+vs+Atom+specification)

---