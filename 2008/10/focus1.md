# Rails 2.2 新特性完整解析（2008）

## 多執行緒時代來臨

### 前言

Rails 2.2 是第一個正式支援多執行緒的版本。這意味著 Rails 應用可以同時處理多個請求，不再受限於單一執行緒的瓶頸。

### 併發處理的底層改進

```ruby
# Rails 2.2 以前的限制：每個請求一個程序
# Rails 2.2 開始：真正的多執行緒支援

# config/environment.rb
Rails::Initializer.run do |config|
  config.threadsafe!
end

# 在 ActionController 中使用執行緒
class ApplicationController < ActionController::Base
  def fetch_data
    @data = Thread.current[:cache] ||= fetch_from_external_api
  end
end
```

### Passenger + threads 的完美結合

```bash
# 使用 Phusion Passenger 啟用執行緒模式
# 在 nginx.conf 中設定：
worker_processes 1;
thread_pool_size 16;
```

### 效能提升

根據社群測試，在多核伺服器上，啟用執行緒模式的 Rails 2.2 處理器吞吐量提升可達 3-5 倍。

## i18n 國際化成為核心功能

### 翻译檔案結構

```ruby
# config/locales/zh-TW.yml
zh-TW:
  hello: "你好"
  messages:
    welcome: "歡迎 %{name}"
    goodbye: "再見"

# 使用翻譯
t("hello")                    # => "你好"
t("messages.welcome", name: "小明")  # => "歡迎小明"
```

### 多語言支援的底層實作

Rails 2.2 的 i18n 功能基於 GetText 標準，並提供了灵活的插入式架構，支援多種後端儲存（YAML、資料庫、GetText 檔案）。

## 歐元符號問題的解決

Rails 2.2 修正了長久以來的歐元符號編碼問題，使用 UTF-8 編碼時不再出現亂碼。

---

**下一步**：[Ruby 1.9 新功能與效能改進（2008）](focus2.md)

## 延伸閱讀

- [Rails 2.2 Thread Safety](https://www.google.com/search?q=Rails+2.2+thread+safety+concurrency)
- [Rails I18n Implementation](https://www.google.com/search?q=Rails+i18n+internationalization+2008)
- [Ruby Enterprise Edition Threading](https://www.google.com/search?q=Ruby+Enterprise+Edition+threading+2008)