#!/usr/bin/env node

function demo() {
  console.log('=== 事件處理機制範例 ===\n');

  console.log('1. 事件監聽器：');
  console.log('   element.addEventListener("event", callback)');
  console.log('   element.removeEventListener("event", callback)');

  console.log('\n2. 事件類型：');
  const events = [
    { type: 'click', desc: '點擊' },
    { type: 'dblclick', desc: '雙擊' },
    { type: 'mouseenter', desc: '滑鼠進入' },
    { type: 'mouseleave', desc: '滑鼠離開' },
    { type: 'keydown', desc: '鍵盤按下' },
    { type: 'keyup', desc: '鍵盤放開' },
    { type: 'submit', desc: '表單提交' },
    { type: 'focus', desc: '獲得焦點' },
    { type: 'blur', desc: '失去焦點' },
    { type: 'resize', desc: '視窗調整' },
    { type: 'scroll', desc: '捲動' },
    { type: 'load', desc: '載入完成' }
  ];

  events.forEach(e => {
    console.log(`   ${e.type}: ${e.desc}`);
  });

  console.log('\n3. 事件物件屬性：');
  console.log('   event.target：觸發事件的元素');
  console.log('   event.currentTarget：當前處理事件的元素');
  console.log('   event.type：事件類型');
  console.log('   event.clientX/Y：滑鼠座標');
  console.log('   event.key：按鍵值');

  console.log('\n4. 事件委託：');
  console.log('   好處：效能更好、可處理動態元素');
  console.log('   原理：利用事件冒泡');

  console.log('\n=== 實作：待辦事項清單事件 ===');
  const todos = ['買早餐', '寫程式', '運動'];
  console.log('\n清單點擊事件處理：');
  todos.forEach((todo, index) => {
    console.log(`   #${index + 1} "${todo}" - 點擊時標記完成`);
  });

  console.log('\n5. 事件阻止：');
  console.log('   event.preventDefault()：阻止預設行為');
  console.log('   return false：在 jQuery 中阻止預設');
  console.log('   event.stopPropagation()：阻止冒泡');
}

if (require.main === module) {
  demo();
}

module.exports = { demo };