// ui-demo.js - UI 元件使用範例
function demo() {
  console.log('=== Android UI 元件範例 ===');
  console.log('Layout：LinearLayout, RelativeLayout, FrameLayout');
  console.log('TextView：顯示文字');
  console.log('Button：按鈕元件');
  console.log('EditText：文字輸入');
  console.log('ListView：列表顯示');
  console.log('Adapter：資料與 UI 的橋樑');
}

if (typeof module !== 'undefined' && module.exports) {
  module.exports = { demo };
}