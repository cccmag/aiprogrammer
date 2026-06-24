#!/usr/bin/env node

function demo() {
  console.log('=== Express REST API 範例 ===\n');

  const users = [
    { id: 1, name: '王小明', email: 'wang@example.com' },
    { id: 2, name: '李小華', email: 'lee@example.com' },
    { id: 3, name: '陳大同', email: 'chen@example.com' }
  ];

  console.log('1. GET /users - 取得所有使用者');
  console.log(JSON.stringify({ users, count: users.length }, null, 2));

  console.log('\n2. GET /users/:id - 取得單一使用者');
  console.log(JSON.stringify({ user: users[0] }, null, 2));

  console.log('\n3. POST /users - 建立使用者');
  const newUser = { id: 4, name: '張小美', email: 'zhang@example.com' };
  console.log(JSON.stringify({ created: true, user: newUser }, null, 2));

  console.log('\n4. PUT /users/:id - 更新使用者');
  const updated = { ...users[0], name: '王小明 Jr.' };
  console.log(JSON.stringify({ updated: true, user: updated }, null, 2));

  console.log('\n5. DELETE /users/:id - 刪除使用者');
  console.log(JSON.stringify({ deleted: true, id: 1 }, null, 2));

  console.log('\n=== 執行 curl 命令 ===');
  console.log('curl http://localhost:3000/api/users');
  console.log('curl http://localhost:3000/api/users/1');
  console.log('curl -X POST http://localhost:3000/api/users -H "Content-Type: application/json" -d \'{"name":"張小美","email":"zhang@example.com"}\'');
}

if (require.main === module) {
  demo();
}

module.exports = { demo };