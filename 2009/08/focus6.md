# 持續整合與測試覆蓋率：CI/CD 基礎

## 持續整合的概念

### 什麼是持續整合？

持續整合（Continuous Integration，CI）是一種軟體開發實踐，開發者每天都會將程式碼整合到共享儲存庫中，每次整合都會自動觸發建置和測試。

```
持續整合流程：

┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐
│  開發者   │───►│  推送    │───►│  CI 伺服器│───►│  建置    │
│  提交     │    │  程式碼   │    │  偵測變更 │    │  + 測試  │
└──────────┘    └──────────┘    └──────────┘    └──────────┘
                                                        │
                    ┌───────────────────────────────────┘
                    ▼
               ┌──────────┐
               │  回饋    │
               │  報告    │
               └──────────┘
```

### CI 的核心原則

```markdown
持續整合原則：

1. 頻繁整合
   - 每天至少整合一次
   - 不要等一週才合併

2. 自動化建置
   - 一鍵建置整個專案
   - 消除手動步驟

3. 自動化測試
   - 每次建置都執行測試
   - 測試必須快速

4. 快速反饋
   - 建置失敗立即通知
   - 讓問題儘早暴露
```

## CI 伺服器

### 2009 年的 CI 工具

| 工具 | 語言 | 特點 |
|------|------|------|
| Hudson | Java | 2005年發布，易於使用 |
| Jenkins | Java | Hudson 分支，2009年 |
| CruiseControl | Java | 最早的 CI 工具之一 |
| TeamCity | Java | JetBrains 開發 |
| Travis CI | Ruby | 2009年，與 GitHub 整合 |
| Buildbot | Python | Python 專案首選 |
| Apache Gump | Java | Java 專案持續建置 |

### Hudson/Jenkins

```xml
<!-- Hudson 配置 -->
<hudson>
  <numExecutors>2</numExecutors>
  <mode>NORMAL</mode>
  <scmCheckoutRetryCount>2</scmCheckoutRetryCount>

  <builders>
    <hudson.tasks.Shell>
      <command>
        cd /path/to/project
        mvn clean test
      </command>
    </hudson.tasks.Shell>
  </builders>

  <publishers>
    <hudson.plugins.htmlpublisher.HtmlPublisher>
      <reportTargets>
        <target>
          <reportDir>coverage</reportDir>
          <reportName>Coverage Report</reportName>
        </target>
      </reportTargets>
    </hudson.plugins.htmlpublisher.HtmlPublisher>
  </publishers>

  <buildWrappers>
    <hudson.plugins.rake.RakeBuilder>
      <rakefile>Rakefile</rakefile>
      <rakeInstallation>(Default)</rakeInstallation>
    </hudson.plugins.rake.RakeBuilder>
  </buildWrappers>
</hudson>
```

### Travis CI

```yaml
# .travis.yml
language: ruby
rvm:
  - 1.9.1
  - 1.8.7

env:
  - DB=mysql
  - DB=postgresql

script:
  - RAILS_ENV=test bundle exec rake db:migrate
  - bundle exec rspec spec/

after_script:
  - COVERAGE=true bundle exec coveralls push
```

## 測試覆蓋率

### 什麼是測試覆蓋率？

測試覆蓋率衡量的是測試執行程式碼的比例。

```python
# 覆蓋率計算
code = """
def add(a, b):
    return a + b

def subtract(a, b):
    return a - b
"""

# 如果只測試 add，覆蓋率是 50%
test = """
def test_add():
    assert add(1, 2) == 3
"""
```

### 覆蓋率工具

| 語言 | 工具 |
|------|------|
| Ruby | SimpleCov, RCov |
| Python | coverage.py |
| Java | JaCoCo, Cobertura |
| JavaScript | Istanbul, Blanket.js |
| C/C++ | gcov, lcov |

### Ruby RCov

```ruby
# SimpleCov 示例
require 'simplecov'
SimpleCov.start do
  add_filter '/spec/'
  add_filter '/config/'
end

# .rspec 配置
--color
--format documentation
--coverage

# Rake 任務
namespace :ci do
  task :coverage do
    ENV['COVERAGE'] = 'true'
    Rake::Task['spec'].invoke
  end
end
```

### Python coverage.py

```bash
# 使用 coverage.py
$ coverage run tests.py
$ coverage report
Name          Stmts   Miss  Cover
---------------------------------
my_module        20      4    80%

$ coverage html  # 生成 HTML 報告
```

## 自動化部署

### 持續部署的概念

```markdown
CI/CD 流水線：

原始碼 ──► 建置 ──► 測試 ──► 部署
              │        │        │
              ▼        ▼        ▼
           編譯     單元測試   預備環境
                     整合測試   生產環境
                     E2E 測試

自動化程度：
- CI：只到測試
- CD：到部署
-_continuous Delivery：手動核准部署
- Continuous Deployment：全自動部署
```

### 部署自動化工具（2009年）

```markdown
部署工具：

1. Capistrano (Ruby)
   - SSH 遠端部署
   - 支援迴滾

2. Fabric (Python)
   - 簡單的 SSH 工具
   - 適合 Python 專案

3. Ant (Java)
   - Java 建置工具
   - 複雜的部署腳本

4. MSBuild (C#)
   - Visual Studio 建置系統
   - .NET 部署
```

### Capistrano 示例

```ruby
# config/deploy.rb
set :application, "my_app"
set :repository,  "git@github.com:user/my_app.git"
set :deploy_to,  "/var/www/my_app"
set :scm, :git
server "example.com", :web, :app, :db, :primary: true

namespace :deploy do
  task :restart do
    run "sudo service apache2 restart"
  end

  task :migrate do
    run "cd #{current_path} && rake db:migrate"
  end
end

after "deploy:update", "deploy:migrate"
after "deploy:update", "deploy:restart"
```

## 測試金字塔與 CI

### 測試策略

```
測試金字塔：

              ▲
             /│\
            / │ \          E2E 測試
           /  │  \         （少量）
          /───┼───\       整合測試
         /    │    \      （適量）
        /─────┼─────\    單元測試
       /      │      \   （大量）
      └───────┴───────┘

CI 配置：
- 單元測試：每次提交
- 整合測試：每次建置
- E2E 測試：每天/每發布
```

### CI 環境設定

```ruby
# spec/spec_helper.rb
RSpec.configure do |config|
  # 隔離測試資料庫
  config.before(:suite) do
    DatabaseCleaner.strategy = :transaction
    DatabaseCleaner.clean_with(:truncation)
  end

  config.around(:each) do |example|
    DatabaseCleaner.cleaning do
      example.run
    end
  end

  # 模擬時間
  config.include(ActiveSupport::Testing::TimeHelpers)

  # 隔離外部 API 呼叫
  WebMock.disable_net_connect!(allow_localhost: true)
end
```

## 失敗處理

### 建置失敗通知

```ruby
# Slack 通知
namespace :ci do
  task :notify_failure do
    if ENV['BUILD_STATUS'] == 'FAILURE'
      SlackNotifier.ping(
        "Build ##{ENV['BUILD_NUMBER']} failed!",
        channel: '#ci',
        webhook: ENV['SLACK_WEBHOOK']
      )
    end
  end
end

after 'deploy:failed' do
  Rake::Task['ci:notify_failure'].invoke
end
```

### 自動迴滾

```bash
#!/bin/bash
# deploy.sh

BRANCH=${1:-master}
DEPLOY_DIR="/var/www/my_app"

# 部署
cd $DEPLOY_DIR
git pull origin $BRANCH
bundle install
rake db:migrate

# 測試
if rake test:integration; then
  echo "Deployment successful"
else
  echo "Deployment failed, rolling back..."
  cap production deploy:rollback
  exit 1
fi
```

## 結語

持續整合和測試覆蓋率是將 TDD 規模化的關鍵。2009 年，這些實踐正在從大型企業走向小型團隊。

下一篇文章將討論 TDD 的現在與未來。

---

## 延伸閱讀

- [持續整合概念](https://www.google.com/search?q=continuous+integration+concepts)
- [Jenkins/Hudson 教程](https://www.google.com/search?q=Jenkins+tutorial+2009)
- [測試覆蓋率工具](https://www.google.com/search?q=test+coverage+tools)
- [CI/CD 最佳化](https://www.google.com/search?q=CI+CD+best+practices)

---

*本篇文章為「AI 程式人雜誌 2009 年 8 月號」焦點系列之一。*