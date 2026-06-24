#!/usr/bin/env python3
"""Web API 完整實作範例"""

import json
import time
import hashlib
import secrets
import base64
import requests
from datetime import datetime


def demo_requests():
    """使用 requests 呼叫公開 API"""
    print("=== requests 範例 ===")
    url = "https://jsonplaceholder.typicode.com/posts"
    params = {"userId": 1, "_limit": 3}
    headers = {"User-Agent": "WebAPIDemo/1.0"}
    resp = requests.get(url, params=params, headers=headers, timeout=10)
    print(f"狀態碼: {resp.status_code}")
    print(f"URL: {resp.url}")
    posts = resp.json()
    for post in posts:
        print(f"  [{post['id']}] {post['title']}")


def demo_json():
    """JSON 資料處理"""
    print("\n=== JSON 範例 ===")
    data = {
        "name": "Alice",
        "age": 30,
        "skills": ["Python", "API"],
        "active": True,
        "registered": datetime.now().isoformat(),
    }
    json_str = json.dumps(data, ensure_ascii=False, indent=2)
    print("序列化輸出:")
    print(json_str)

    parsed = json.loads(json_str)
    assert parsed["name"] == "Alice"
    print("反序列化驗證通過")


def demo_fastapi_simulation():
    """模擬 FastAPI 風格的 API 處理"""
    print("\n=== FastAPI 模擬範例 ===")

    def validate_item(data: dict) -> dict:
        errors = {}
        if "name" not in data or not isinstance(data["name"], str):
            errors["name"] = "必須是字串"
        if "price" in data:
            try:
                p = float(data["price"])
                if p < 0:
                    errors["price"] = "不能為負數"
            except (ValueError, TypeError):
                errors["price"] = "必須是數字"
        if errors:
            return {"status": 422, "error": "VALIDATION_ERROR",
                    "detail": errors}
        return {"status": 200, "data": data}

    items = []
    item_id = 1

    def create_item(data: dict) -> dict:
        nonlocal item_id
        result = validate_item(data)
        if result["status"] != 200:
            return result
        new_item = {"id": item_id, **data}
        items.append(new_item)
        item_id += 1
        return {"status": 201, "data": new_item}

    def list_items() -> dict:
        return {"status": 200, "data": items}

    def get_item(item_id: int) -> dict:
        for item in items:
            if item["id"] == item_id:
                return {"status": 200, "data": item}
        return {"status": 404, "error": "NOT_FOUND",
                "message": f"物品 {item_id} 不存在"}

    def delete_item(item_id: int) -> dict:
        for i, item in enumerate(items):
            if item["id"] == item_id:
                items.pop(i)
                return {"status": 204}
        return {"status": 404, "error": "NOT_FOUND",
                "message": f"物品 {item_id} 不存在"}

    print("建立物品:")
    resp = create_item({"name": "筆記本", "price": 29.99})
    print(f"  {resp}")

    resp = create_item({"name": "原子筆", "price": 9.99})
    print(f"  {resp}")

    print("\n列出所有物品:")
    resp = list_items()
    for item in resp["data"]:
        print(f"  [{item['id']}] {item['name']} - ${item['price']}")

    print("\n查詢單一物品:")
    resp = get_item(1)
    print(f"  {resp}")

    print("\n查詢不存在的物品:")
    resp = get_item(99)
    print(f"  {resp}")

    print("\n刪除物品:")
    resp = delete_item(1)
    print(f"  刪除結果: {resp}")

    print("\n驗證錯誤:")
    resp = create_item({"name": 123})
    print(f"  {resp}")


def demo_auth():
    """模擬 API 認證機制"""
    print("\n=== API 認證範例 ===")

    def generate_api_key():
        return secrets.token_urlsafe(16)

    def validate_api_key(key: str, valid_keys: set) -> bool:
        return key in valid_keys

    def create_jwt(payload: dict, secret: str) -> str:
        header = json.dumps({"alg": "HS256", "typ": "JWT"})
        payload_str = json.dumps(payload)
        b64_header = base64.urlsafe_b64encode(
            header.encode()).rstrip(b"=").decode()
        b64_payload = base64.urlsafe_b64encode(
            payload_str.encode()).rstrip(b"=").decode()
        signature_input = f"{b64_header}.{b64_payload}"
        signature = hashlib.sha256(
            f"{signature_input}{secret}".encode()).hexdigest()
        return f"{b64_header}.{b64_payload}.{signature}"

    api_key = generate_api_key()
    valid_keys = {api_key}
    print(f"API Key: {api_key}")
    print(f"驗證通過: {validate_api_key(api_key, valid_keys)}")
    print(f"驗證失敗: {validate_api_key('fake-key', valid_keys)}")

    jwt_token = create_jwt(
        {"user_id": 1, "role": "admin"}, "my-secret")
    print(f"JWT Token: {jwt_token}")


def demo_rate_limit():
    """模擬速率限制"""
    print("\n=== 速率限制範例 ===")
    limits = {}
    window = 10
    max_req = 5

    def check_rate_limit(client_id: str) -> dict:
        now = int(time.time())
        key = f"{client_id}:{now // window}"
        count = limits.get(key, 0)
        remaining = max_req - count
        limits[key] = count + 1
        return {"allowed": count < max_req, "remaining": max(remaining, 0)}

    for i in range(7):
        result = check_rate_limit("client-1")
        status = "允許" if result["allowed"] else "拒絕"
        print(f"  請求 {i+1}: {status} (剩餘: {result['remaining']})")


def demo():
    """執行所有範例"""
    demo_requests()
    demo_json()
    demo_fastapi_simulation()
    demo_auth()
    demo_rate_limit()
    print("\n所有範例執行完畢！")


if __name__ == "__main__":
    demo()
