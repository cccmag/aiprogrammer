# 測試驅動開發在 Rails

## 1. Test::Unit 基礎

```ruby
require 'test_helper'

class PostTest < ActiveSupport::TestCase
  test "title is required" do
    post = Post.new(content: "內容")
    assert post.invalid?
    assert post.errors[:title].any?
  end

  test "published scope returns only published posts" do
    Post.create!(title: "Draft", published: false)
    Post.create!(title: "Published", published: true)
    assert_equal 1, Post.published.count
  end
end
```

## 2. Shoulda

```ruby
context "A Post" do
  setup { @post = Post.new(title: "Test") }

  should "require a title" do
    @post.title = nil
    assert @post.invalid?
  end

  should "have a published_at timestamp when published" do
    @post.publish!
    assert_not_nil @post.published_at
  end
end
```

## 3. Fixtures

```yaml
# test/fixtures/posts.yml
one:
  title: MyString
  content: MyText
  author: MyString

two:
  title: MyString2
  content: MyText2
  author: MyString2
```

## 4. 功能測試

```ruby
class PostsControllerTest < ActionController::TestCase
  test "should get index" do
    get :index
    assert_response :success
    assert_not_nil assigns(:posts)
  end

  test "should create post" do
    assert_difference('Post.count') do
      post :create, post: { title: "Test", content: "Content" }
    end
    assert_redirected_to post_path(assigns(:post))
  end
end
```

## 5. 整合測試

```ruby
require 'test_helper'

class PostWorkflowTest < ActionDispatch::IntegrationTest
  test "complete post workflow" do
    get "/posts"
    assert_response :success

    post "/posts", post: { title: "New", content: "Content" }
    assert_redirected_to post_path(assigns(:post))
  end
end
```

---

**參考資料**
- [Rails Testing Guide](https://www.google.com/search?q=Rails+testing+TDD+test+driven)
- [Shoulda Testing Framework](https://www.google.com/search?q=Shoulda+Rails+testing+context)
- [Fixtures in Rails](https://www.google.com/search?q=Rails+fixtures+test+data)