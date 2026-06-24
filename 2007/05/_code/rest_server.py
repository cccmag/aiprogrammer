#!/usr/bin/env python3
"""REST API 伺服器 - Flask 實作"""

from flask import Flask, jsonify, request, abort
from functools import wraps
import time
import hashlib

app = Flask(__name__)

users_db = {
    '1': {'id': '1', 'name': 'John', 'email': 'john@example.com'},
    '2': {'id': '2', 'name': 'Mary', 'email': 'mary@example.com'},
    '3': {'id': '3', 'name': 'Bob', 'email': 'bob@example.com'},
}

posts_db = {
    '1': {'id': '1', 'author_id': '1', 'title': 'Hello World', 'content': 'First post'},
    '2': {'id': '2', 'author_id': '2', 'title': 'REST API', 'content': 'About REST'},
}

def require_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth:
            abort(401, description='Missing authentication')
        if not verify_credentials(auth.username, auth.password):
            abort(401, description='Invalid credentials')
        return f(*args, **kwargs)
    return decorated

def verify_credentials(username, password):
    return username == 'admin' and password == 'secret'

def json_response(data, status=200):
    return jsonify(data), status

@app.route('/api/users', methods=['GET'])
def list_users():
    return json_response({'users': list(users_db.values())})

@app.route('/api/users/<user_id>', methods=['GET'])
def get_user(user_id):
    user = users_db.get(user_id)
    if not user:
        abort(404, description='User not found')
    return json_response(user)

@app.route('/api/users', methods=['POST'])
def create_user():
    data = request.json
    if not data or 'name' not in data:
        abort(400, description='Name is required')

    user_id = str(int(max(users_db.keys(), default='0')) + 1)
    user = {
        'id': user_id,
        'name': data['name'],
        'email': data.get('email', '')
    }
    users_db[user_id] = user
    return json_response(user, 201)

@app.route('/api/users/<user_id>', methods=['PUT'])
def update_user(user_id):
    user = users_db.get(user_id)
    if not user:
        abort(404, description='User not found')

    data = request.json
    user['name'] = data.get('name', user['name'])
    user['email'] = data.get('email', user['email'])
    return json_response(user)

@app.route('/api/users/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    if user_id not in users_db:
        abort(404, description='User not found')
    del users_db[user_id]
    return '', 204

@app.route('/api/posts', methods=['GET'])
def list_posts():
    return json_response({'posts': list(posts_db.values())})

@app.route('/api/posts/<post_id>', methods=['GET'])
def get_post(post_id):
    post = posts_db.get(post_id)
    if not post:
        abort(404, description='Post not found')
    return json_response(post)

@app.route('/api/posts', methods=['POST'])
def create_post():
    data = request.json
    if not data or 'title' not in data:
        abort(400, description='Title is required')

    post_id = str(int(max(posts_db.keys(), default='0')) + 1)
    post = {
        'id': post_id,
        'author_id': data.get('author_id', '1'),
        'title': data['title'],
        'content': data.get('content', '')
    }
    posts_db[post_id] = post
    return json_response(post, 201)

@app.errorhandler(404)
def not_found(e):
    return jsonify({'error': str(e.description)}), 404

@app.errorhandler(400)
def bad_request(e):
    return jsonify({'error': str(e.description)}), 400

@app.errorhandler(401)
def unauthorized(e):
    return jsonify({'error': str(e.description)}), 401

def demo():
    print('REST API 伺服器範例')
    print('=' * 40)
    print()
    print('可用端點：')
    print('  GET    /api/users          - 列出所有用戶')
    print('  POST   /api/users         - 建立新用戶')
    print('  PUT    /api/users/<id>    - 更新用戶')
    print('  DELETE /api/users/<id>    - 刪除用戶')
    print('  GET    /api/posts         - 列出所有文章')
    print('  POST   /api/posts         - 建立新文章')

if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == 'demo':
        demo()
    else:
        print('啟動伺服器在 http://localhost:5000')
        app.run(debug=True, port=5000)