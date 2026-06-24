# 資料庫遷移與版本控制

## 1. Rails 遷移系統

遷移讓資料庫結構變更成為版本控制的一部分：

```bash
# 建立遷移檔案
script/generate migration AddEmailToUsers email:string
```

## 2. 遷移檔案結構

```ruby
class AddEmailToUsers < ActiveRecord::Migration
  def self.up
    create_table :users do |t|
      t.string :name
      t.string :email
      t.timestamps
    end
  end

  def self.down
    drop_table :users
  end
end
```

## 3. 執行遷移

```bash
rake db:migrate          # 執行未套用的遷移
rake db:rollback         # 回滾上一個遷移
rake db:migrate:status   # 查看遷移狀態
```

## 4. 版本化資料庫快照

```bash
# 匯出當前結構為 SQL
rake db:structure:dump

# 從結構檔案載入
rake db:structure:load
```

## 5. 測試資料管理

```ruby
# db/seeds.rb
users = [
  { name: "小明", email: "a@test.com" },
  { name: "大華", email: "b@test.com" }
]

users.each do |u|
  User.find_or_create_by_email(u[:email]) do |user|
    user.name = u[:name]
  end
end
```

```bash
rake db:seed
```

## 6. 多人協作策略

```bash
# 每位開發者獨立遷移
git pull
rake db:migrate

# 合併衝突時
rake db:migrate:down VERSION=20081101120000
rake db:migrate:up VERSION=20081101120000
```

---

**參考資料**
- [Rails Migrations Guide](https://www.google.com/search?q=Rails+database+migrations+guide)
- [Schema Migration Patterns](https://www.google.com/search?q=database+migration+best+practices)
- [Rails DB Version Control](https://www.google.com/search?q=Rails+db+version+control+migrate)