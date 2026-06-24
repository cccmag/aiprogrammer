# RSpec 2.0：更好的測試框架

## RSpec 2.0 的新功能

### 改進的 DSL

```ruby
# RSpec 2.0 的語法

describe User do
  describe "#create" do
    context "with valid attributes" do
      it "creates a new user" do
        expect {
          User.create(name: "張三")
        }.to change(User, :count).by(1)
      end
    end
  end
end
```

### Rack 測試支援

```ruby
# Rails 整合改進
describe UsersController do
  render_views

  it "responds successfully" do
    get :index
    response.should be_success
  end
end
```

## 結語

RSpec 2.0 成為 Ruby 測試的標準框架。

---

*本篇文章為「AI 程式人雜誌 2009 年 10 月號」焦點系列之一。*