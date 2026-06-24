// intent-demo.js - Intent 使用範例展示
function demo() {
  console.log('=== Android Intent 範例展示 ===');
  console.log('明確 Intent：指定目標元件');
  console.log('隱含 Intent：指定動作讓系統選擇');
  console.log('常用動作：VIEW, EDIT, SEND, DIAL');
  console.log('資料傳遞：putExtra(key, value)');
  console.log('結果返回：startActivityForResult');
}

if (typeof module !== 'undefined' && module.exports) {
  module.exports = { demo };
}