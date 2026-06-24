# 部署與伺服器設定

## 1. Capistrano 部署

```ruby
# config/deploy.rb
set :application, "myapp"
set :repository, "git@github.com:user/myapp.git"
set :deploy_to, "/var/www/myapp"
set :scm, :git

server "example.com", :web, :app, :db, primary: true

namespace :deploy do
  task :restart do
    run "touch #{current_release}/tmp/restart.txt"
  end
end
```

## 2. 部署流程

```bash
cap deploy:setup       # 初次設定
cap deploy:check       # 檢查設定
cap deploy             # 部署
cap deploy:rollback    # 回滾
```

## 3. Nginx + Passenger

```nginx
# /etc/nginx/sites-available/myapp
server {
  listen 80;
  server_name myapp.com;
  root /var/www/myapp/current/public;

  passenger_enabled on;
  rails_env production;
}
```

## 4. 資料庫設定

```ruby
# config/database.yml
production:
  adapter: mysql2
  encoding: utf8
  database: myapp_production
  username: deploy
  password: <%= ENV['DB_PASSWORD'] %>
  host: localhost
```

## 5. 環境變數

```bash
# ~/.bashrc 或 /etc/environment
export DB_PASSWORD="secret"
export SECRET_KEY_BASE="..."
export RAILS_ENV=production
```

## 6. Monit 監控

```ruby
# /etc/monit/conf.d/nginx
check process nginx with pidfile /var/run/nginx.pid
  start program = "/etc/init.d/nginx start"
  stop program = "/etc/init.d/nginx stop"
```

---

**參考資料**
- [Capistrano Deployment](https://www.google.com/search?q=Capistrano+Rails+deployment+2008)
- [Nginx Passenger Rails](https://www.google.com/search?q=Nginx+Passenger+Rails+production)
- [Rails Production Setup](https://www.google.com/search?q=Rails+production+server+setup)