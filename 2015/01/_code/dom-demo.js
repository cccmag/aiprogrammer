#!/usr/bin/env node

function demo() {
  console.log('=== DOM 查詢與操作範例 ===\n');

  const items = ['HTML5', 'CSS3', 'JavaScript ES6', '響應式設計', 'Web APIs'];

  console.log('1. 建立元素：');
  items.forEach((item, index) => {
    console.log(`   建立 <li> 元素: ${item}`);
  });

  console.log('\n2. DOM 遍歷：');
  console.log('   - getElementById()：根據 ID 查詢');
  console.log('   - getElementsByClassName()：根據類別查詢');
  console.log('   - querySelector()：CSS 選擇器查詢');
  console.log('   - querySelectorAll()：查詢所有符合元素');

  console.log('\n3. 元素操作：');
  console.log('   - appendChild()：插入子元素');
  console.log('   - removeChild()：移除子元素');
  console.log('   - classList.add/remove/toggle()：操作類別');

  console.log('\n4. 屬性操作：');
  console.log('   - setAttribute()：設定屬性');
  console.log('   - getAttribute()：取得屬性');
  console.log('   - style.xxx：直接操作樣式');

  console.log('\n=== 模擬輸出結果 ===');
  console.log('外層容器: <ul id="list" class="container">');
  items.forEach((item, index) => {
    console.log(`  <li class="item" data-index="${index}">${item}</li>`);
  });
  console.log('</ul>');

  console.log('\n=== 事件處理 ===');
  console.log('addEventListener("click", handler)');
  console.log('事件委託：父元素監聽子元素事件');
  console.log('event.preventDefault()：阻止預設行為');
  console.log('event.stopPropagation()：停止事件冒泡');
}

if (require.main === module) {
  demo();
}

module.exports = { demo };