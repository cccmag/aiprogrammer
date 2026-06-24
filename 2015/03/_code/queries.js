#!/usr/bin/env node

function demo() {
  console.log('=== 常用 SQL 查詢範例 ===\n');

  const users = [
    { id: 1, name: '王小明', email: 'wang@example.com', age: 25, country: 'Taiwan' },
    { id: 2, name: '李小華', email: 'lee@example.com', age: 30, country: 'Taiwan' },
    { id: 3, name: '陳大同', email: 'chen@example.com', age: 35, country: 'USA' }
  ];

  const orders = [
    { id: 1, user_id: 1, total: 1000, created_at: '2015-03-01' },
    { id: 2, user_id: 1, total: 2000, created_at: '2015-03-15' },
    { id: 3, user_id: 2, total: 500, created_at: '2015-03-10' }
  ];

  console.log('1. 基本 SELECT：');
  console.log("SELECT * FROM users;");
  console.log(JSON.stringify(users, null, 2));

  console.log('\n2. WHERE 條件：');
  console.log("SELECT * FROM users WHERE age >= 18;");
  const adults = users.filter(u => u.age >= 18);
  console.log(JSON.stringify(adults, null, 2));

  console.log('\n3. JOIN 查詢：');
  console.log("SELECT u.name, o.total FROM users u INNER JOIN orders o ON u.id = o.user_id;");
  const joined = users.map(u => {
    const userOrders = orders.filter(o => o.user_id === u.id);
    return {
      name: u.name,
      orders: userOrders.length,
      total: userOrders.reduce((sum, o) => sum + o.total, 0)
    };
  });
  console.log(JSON.stringify(joined, null, 2));

  console.log('\n4. 聚合查詢：');
  console.log("SELECT country, COUNT(*), AVG(age) FROM users GROUP BY country;");
  const grouped = {};
  users.forEach(u => {
    if (!grouped[u.country]) {
      grouped[u.country] = { country: u.country, count: 0, ages: [] };
    }
    grouped[u.country].count++;
    grouped[u.country].ages.push(u.age);
  });
  const aggregated = Object.values(grouped).map(g => ({
    country: g.country,
    count: g.count,
    avg_age: (g.ages.reduce((a, b) => a + b, 0) / g.count).toFixed(1)
  }));
  console.log(JSON.stringify(aggregated, null, 2));

  console.log('\n5. 子查詢：');
  console.log("SELECT * FROM users WHERE age > (SELECT AVG(age) FROM users);");
  const avgAge = users.reduce((sum, u) => sum + u.age, 0) / users.length;
  const aboveAvg = users.filter(u => u.age > avgAge);
  console.log(`平均年齡: ${avgAge.toFixed(1)}`);
  console.log(JSON.stringify(aboveAvg, null, 2));
}

if (require.main === module) {
  demo();
}

module.exports = { demo };