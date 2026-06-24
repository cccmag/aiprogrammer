#!/usr/bin/env node

function demo() {
  console.log('=== REST API 用戶端測試 ===\n');

  const baseUrl = 'http://localhost:3000/api';

  console.log('測試場景：');
  console.log('1. 取得所有使用者');
  console.log(`   GET ${baseUrl}/users`);

  console.log('\n2. 建立新使用者');
  console.log(`   POST ${baseUrl}/users`);
  console.log('   Body:', JSON.stringify({ name: '測試用戶', email: 'test@example.com' }, null, 2));

  console.log('\n3. 取得單一使用者');
  console.log(`   GET ${baseUrl}/users/1`);

  console.log('\n4. 更新使用者');
  console.log(`   PUT ${baseUrl}/users/1`);
  console.log('   Body:', JSON.stringify({ name: '更新後的名稱' }, null, 2));

  console.log('\n5. 刪除使用者');
  console.log(`   DELETE ${baseUrl}/users/1`);

  console.log('\n=== 預期回應格式 ===');
  console.log(JSON.stringify({
    success: true,
    data: { id: 1, name: '範例用戶' },
    message: '操作成功'
  }, null, 2));
}

if (require.main === module) {
  demo();
}

module.exports = { demo };