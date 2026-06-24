#!/usr/bin/env python3
"""社群網路 API 模擬器"""

import json
import time

class SocialNetwork:
    def __init__(self):
        self.users = {}
        self.friendships = {}
        self.posts = []
        self.next_post_id = 1

    def create_user(self, name, email):
        user_id = len(self.users) + 1
        self.users[user_id] = {
            'id': user_id,
            'name': name,
            'email': email,
            'created_at': time.time()
        }
        self.friendships[user_id] = set()
        return user_id

    def add_friend(self, user_id, friend_id):
        if user_id in self.friendships and friend_id in self.users:
            self.friendships[user_id].add(friend_id)
            self.friendships[friend_id].add(user_id)
            return True
        return False

    def get_friends(self, user_id):
        if user_id not in self.friendships:
            return []
        return list(self.friendships[user_id])

    def post_status(self, user_id, message):
        post = {
            'id': self.next_post_id,
            'user_id': user_id,
            'message': message,
            'timestamp': time.time(),
            'likes': 0
        }
        self.posts.append(post)
        self.next_post_id += 1
        return post

    def get_feed(self, user_id):
        friends = self.friendships.get(user_id, set())
        user_posts = [p for p in self.posts if p['user_id'] in friends or p['user_id'] == user_id]
        return sorted(user_posts, key=lambda x: x['timestamp'], reverse=True)

def demo():
    print('社群網路 API 演示')
    print('=' * 40)

    sn = SocialNetwork()

    print('\n1. 建立使用者')
    alice_id = sn.create_user('Alice', 'alice@example.com')
    bob_id = sn.create_user('Bob', 'bob@example.com')
    print(f'   Alice ID: {alice_id}, Bob ID: {bob_id}')

    print('\n2. 成為好友')
    sn.add_friend(alice_id, bob_id)
    print(f'   Alice 的好友: {sn.get_friends(alice_id)}')

    print('\n3. 發布動態')
    sn.post_status(alice_id, 'Hello, World!')
    sn.post_status(bob_id, 'Hi there!')
    print('   已發布兩條動態')

    print('\n4. 獲取動態')
    feed = sn.get_feed(alice_id)
    print(f'   Alice 的動態: {len(feed)} 條')

if __name__ == '__main__':
    demo()