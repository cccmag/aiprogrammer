#!/usr/bin/env node

function demo() {
  console.log('=== Fetch API 範例 ===\n');

  console.log('1. 基本 GET 請求：');
  console.log(`
fetch('/api/users')
  .then(response => response.json())
  .then(data => console.log(data))
  .catch(error => console.error(error));
`);

  console.log('2. POST 請求：');
  console.log(`
fetch('/api/users', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({ name: 'John', email: 'john@example.com' })
})
  .then(response => response.json())
  .then(data => console.log(data));
`);

  console.log('3. 錯誤處理：');
  console.log(`
if (!response.ok) {
  throw new Error(\`HTTP \${response.status}\`);
}
`);

  console.log('4. async/await 語法：');
  console.log(`
async function loadData() {
  try {
    const response = await fetch('/api/data');
    const data = await response.json();
    return data;
  } catch (error) {
    console.error(error);
  }
}
`);

  console.log('=== 模擬 API 呼叫 ===\n');

  const mockUsers = [
    { id: 1, name: '王小明', email: 'wang@example.com' },
    { id: 2, name: '李小華', email: 'lee@example.com' },
    { id: 3, name: '陳大同', email: 'chen@example.com' }
  ];

  console.log('GET /api/users =>');
  console.log(JSON.stringify(mockUsers, null, 2));

  console.log('\nPOST /api/users =>');
  const newUser = { id: 4, name: '張小美', email: 'zhang@example.com' };
  console.log('Request:', JSON.stringify({ name: '張小美', email: 'zhang@example.com' }));
  console.log('Response:', JSON.stringify(newUser, null, 2));
}

if (require.main === module) {
  demo();
}

module.exports = { demo };