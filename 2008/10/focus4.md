# ActiveRecord 與資料庫抽象層（2008）

## ORM 的力量

### 前言

ActiveRecord 是 Rails 的 ORM（Object-Relational Mapping）實作，它將資料庫表格映射為 Ruby 物件，讓開發者可以用物件導向的方式操作資料庫。

### 基本 CRUD 操作

```ruby
# Create
user = User.create(name: "王小明", email: "wang@example.com")

# Read
user = User.find(1)
users = User.where(active: true).limit(10)

# Update
user.update(name: "大明")
user.update_attributes(name: "新名字")

# Delete
user.destroy
User.delete_all(["active = ?", false])
```

## 遷移（Migrations）

### 建立遷移

```bash
# 建立遷移檔案
script/generate migration AddPhoneToUsers phone:string
```

### 遷移語法

```ruby
class AddPhoneToUsers < ActiveRecord::Migration
  def self.up
    add_column :users, :phone, :string, limit: 20
    add_index :users, :phone
  end

  def self.down
    remove_column :users, :phone
  end
end

# 使用 change 方法（Rails 3.1+）
def change
  add_column :users, :phone, :string
end
```

### 資料表操作

```ruby
create_table :posts do |t|
  t.string :title, null: false
  t.text :content
  t.references :user  # 外部鍵

  t.timestamps  # created_at, updated_at
end

# 修改現有資料表
change_table :posts do |t|
  t.remove :subtitle
  t.string :slug
  t.index :slug
end
```

## 查詢介面

### 方法鏈

```ruby
Post.where("published = ? AND created_at > ?", true, 1.month.ago)
    .includes(:user, :comments)
    .order("views DESC")
    .limit(20)
```

### 命名範圍（Scopes）

```ruby
class Post < ActiveRecord::Base
  scope :published, where(published: true)
  scope :recent, order("created_at DESC")
  scope :by_author, ->(user) { where(user_id: user.id) }

  scope :search, ->(q) {
    where("title LIKE ? OR content LIKE ?", "%#{q}%", "%#{q}%")
  }
end

Post.published.recent.search("Rails")
```

## 驗證（Validations）

```ruby
class User < ActiveRecord::Base
  validates :email, presence: true, uniqueness: true,
                    format: { with: /\A[\w+\-.]+@[\w+\-.]+\.[a-z]+\z/ }
  validates :password, length: { in: 6..20 }, confirmation: true
  validates :age, numericality: { greater_than: 0, less_than: 150 }

  validate :custom_validation

  def custom_validation
    if name.present? && name.length < 2
      errors.add(:name, "太短了")
    end
  end
end
```

## 回呼（Callbacks）

```ruby
class User < ActiveRecord::Base
  before_validation :normalize_email
  after_create :send_welcome_email
  after_save :cache_cleanup

  private

  def normalize_email
    self.email = email.downcase.strip
  end

  def send_welcome_email
    UserMailer.welcome(self).deliver
  end
end
```

---

**下一步**：[Rails 路由與 RESTful 設計（2008）](focus5.md)

## 延伸閱讀

- [ActiveRecord Query Interface](https://www.google.com/search?q=ActiveRecord+query+interface+Rails)
- [Rails Migrations Best Practices](https://www.google.com/search?q=Rails+migrations+best+practices)
- [ActiveRecord Validations](https://www.google.com/search?q=ActiveRecord+validations+callbacks)