#!/usr/bin/env python3
"""MiniAPI - Simplified REST API Framework Demo"""

import json


def demo():
    print("\n" + "#" * 60)
    print("# MiniAPI - REST API Framework Demo")
    print("#" * 60 + "\n")

    # 模擬的 REST API
    users = []

    # POST /users
    print("POST /users - Create user")
    user = {"id": 1, "name": "張三"}
    users.append(user)
    print(f"  Created: {user}")
    print(f"  Response: 201 Created\n")

    # GET /users
    print("GET /users - List users")
    print(f"  Response: 200 OK - {json.dumps(users, ensure_ascii=False)}\n")

    # GET /users/1
    print("GET /users/1 - Get user 1")
    print(f"  Response: 200 OK - {json.dumps(users[0], ensure_ascii=False)}\n")

    print("Test complete!")


if __name__ == "__main__":
    demo()