# 串接公開 API 實戰

## 為什麼要串接公開 API？

公開 API 是現代軟體開發的寶貴資源。無論是 GitHub、天氣資料、地理位置、社群媒體還是 AI 服務，公開 API 讓開發者可以快速整合外部功能，無需從頭打造。

## 實戰一：GitHub API 取得使用者資訊

```python
import requests

def get_github_profile(username: str):
    url = f"https://api.github.com/users/{username}"
    headers = {"Accept": "application/vnd.github.v3+json"}
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        return {"error": "無法取得使用者資料"}

    data = response.json()
    return {
        "login": data["login"],
        "name": data["name"],
        "bio": data["bio"],
        "public_repos": data["public_repos"],
        "followers": data["followers"],
        "following": data["following"],
        "avatar": data["avatar_url"],
    }

profile = get_github_profile("octocat")
for key, value in profile.items():
    print(f"{key}: {value}")
```

## 實戰二：JSONPlaceholder 待辦事項管理

```python
import requests

BASE = "https://jsonplaceholder.typicode.com"

def fetch_todos(user_id: int = None):
    url = f"{BASE}/todos"
    if user_id:
        url += f"?userId={user_id}"
    response = requests.get(url)
    response.raise_for_status()
    return response.json()

def create_todo(title: str, user_id: int = 1):
    todo = {"title": title, "completed": False, "userId": user_id}
    response = requests.post(f"{BASE}/todos", json=todo)
    return response.json()

def complete_todo(todo_id: int):
    response = requests.patch(f"{BASE}/todos/{todo_id}",
        json={"completed": True})
    return response.json()

# 使用範例
todos = fetch_todos(user_id=1)
print(f"使用者 1 有 {len(todos)} 個待辦事項")
incomplete = [t for t in todos if not t["completed"]]
print(f"未完成：{len(incomplete)} 個")

new = create_todo("學習 Python API")
print(f"新增待辦事項 ID：{new['id']}")

completed = complete_todo(1)
print(f"已完成：{completed['completed']}")
```

## 實戰三：OpenWeatherMap 天氣 API

```python
import requests

API_KEY = "your-api-key"

def get_weather(city: str):
    url = "https://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": city,
        "appid": API_KEY,
        "units": "metric",
        "lang": "zh_tw"
    }
    response = requests.get(url, params=params)
    if response.status_code != 200:
        return {"error": "無法取得天氣資料"}

    data = response.json()
    return {
        "city": data["name"],
        "temperature": data["main"]["temp"],
        "feels_like": data["main"]["feels_like"],
        "humidity": data["main"]["humidity"],
        "description": data["weather"][0]["description"],
        "wind_speed": data["wind"]["speed"],
    }

# 模擬測試（不實際呼叫 API）
mock_data = {
    "name": "Taipei", "main": {"temp": 25.5, "feels_like": 26,
    "humidity": 75}, "weather": [{"description": "多雲"}],
    "wind": {"speed": 3.5}
}
weather = {
    "city": mock_data["name"],
    "temperature": mock_data["main"]["temp"],
    "feels_like": mock_data["main"]["feels_like"],
    "humidity": mock_data["main"]["humidity"],
    "description": mock_data["weather"][0]["description"],
    "wind_speed": mock_data["wind"]["speed"],
}
print(f"{weather['city']} 天氣：{weather['description']}")
print(f"溫度：{weather['temperature']}°C")
```

## 實戰四：結合多個 API 的應用

```python
import requests

def get_user_info(github_username: str):
    """結合 GitHub API 和自訂資料"""
    result = {"github": {}, "posts": []}

    # 取得 GitHub 資料
    gh_resp = requests.get(
        f"https://api.github.com/users/{github_username}")
    if gh_resp.status_code == 200:
        gh_data = gh_resp.json()
        result["github"] = {
            "name": gh_data["name"],
            "bio": gh_data["bio"],
            "repos": gh_data["public_repos"],
        }

    # 取得假資料的貼文
    posts_resp = requests.get(
        "https://jsonplaceholder.typicode.com/posts",
        params={"userId": 1}
    )
    if posts_resp.status_code == 200:
        result["posts"] = [
            {"title": p["title"], "body": p["body"]}
            for p in posts_resp.json()[:3]
        ]

    return result

info = get_user_info("octocat")
for section, data in info.items():
    print(f"\n{section.upper()}:")
    if isinstance(data, dict):
        for k, v in data.items():
            print(f"  {k}: {v}")
    else:
        for item in data:
            print(f"  - {item['title']}")
```

## 實戰五：建立 FastAPI 代理

```python
from fastapi import FastAPI, HTTPException
import httpx
import asyncio

app = FastAPI()

@app.get("/proxy/github/{username}")
async def proxy_github(username: str):
    """代理 GitHub API 請求（隱藏 API 金鑰）"""
    async with httpx.AsyncClient() as client:
        resp = await client.get(
            f"https://api.github.com/users/{username}",
            headers={"Accept": "application/vnd.github.v3+json"}
        )
    if resp.status_code != 200:
        raise HTTPException(resp.status_code, "GitHub API 錯誤")
    data = resp.json()
    return {
        "username": data["login"],
        "name": data["name"],
        "public_repos": data["public_repos"],
    }

@app.get("/aggregate/user/{username}")
async def aggregate_user_data(username: str):
    """彙總多個來源的使用者資料"""
    async with httpx.AsyncClient() as client:
        gh_task = client.get(
            f"https://api.github.com/users/{username}")
        todo_task = client.get(
            "https://jsonplaceholder.typicode.com/todos",
            params={"userId": 1}
        )
        gh_resp, todo_resp = await asyncio.gather(gh_task, todo_task)

    result = {}
    if gh_resp.status_code == 200:
        gh = gh_resp.json()
        result["github"] = {"name": gh["name"], "bio": gh["bio"]}
    if todo_resp.status_code == 200:
        todos = todo_resp.json()
        result["tasks"] = {
            "total": len(todos),
            "completed": sum(1 for t in todos if t["completed"])
        }
    return result
```

## 速率限制與快取

```python
import requests
from datetime import datetime, timedelta

class CachedAPI:
    def __init__(self, cache_duration: int = 60):
        self.cache = {}
        self.cache_duration = cache_duration

    def get(self, url: str):
        now = datetime.now()
        if url in self.cache:
            data, expiry = self.cache[url]
            if now < expiry:
                return data

        response = requests.get(url, headers={
            "User-Agent": "MyApp/1.0"
        })
        if response.status_code == 200:
            self.cache[url] = (
                response.json(),
                now + timedelta(seconds=self.cache_duration)
            )
            return response.json()
        return {"error": f"HTTP {response.status_code}"}

api = CachedAPI(cache_duration=30)
data1 = api.get("https://api.github.com/users/octocat")
data2 = api.get("https://api.github.com/users/octocat")  # 從快取讀取
print(data1["login"] if "login" in data1 else data1)
```

---

## 延伸閱讀

- [GitHub REST API 文件](https://www.google.com/search?q=GitHub+REST+API+documentation)
- [Public APIs 列表](https://www.google.com/search?q=public+APIs+list)
- [API 整合最佳實踐](https://www.google.com/search?q=API+integration+best+practices)
