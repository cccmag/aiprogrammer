# HTTP/1.1 與 WebDAV：企業級網路協定

## 前言

WebDAV（Web-based Distributed Authoring and Versioning）是 HTTP/1.1 的擴展，支援協作式文件編輯。

## WebDAV 方法

```http
PROPFIND /documents/ HTTP/1.1
Host: server.example.com

HTTP/1.1 207 Multi-Status
Content-Type: application/xml

<d:propfind xmlns:d="DAV:">
  <d:prop>
    <d:displayname>Documents</d:displayname>
    <d:getcontentlength>4096</d:getcontentlength>
  </d:prop>
</d:propfind>
```

## 結語

WebDAV 在企業文件管理系統中有廣泛應用。

---

## 延伸閱讀

- [WebDAV+protocol+2007](https://www.google.com/search?q=WebDAV+protocol+2007)

---