// activity-demo.js - Activity 生命週期展示
function demo() {
  console.log('=== Android Activity 生命週期展示 ===');
  console.log('onCreate() - Activity 建立的初始化');
  console.log('onStart() - Activity 變得可見');
  console.log('onResume() - Activity 可以互動');
  console.log('onPause() - Activity 失去焦點');
  console.log('onStop() - Activity 完全不可見');
  console.log('onDestroy() - Activity 被銷毀');
  console.log('onRestart() - 從 onStop 恢復');
}

if (typeof module !== 'undefined' && module.exports) {
  module.exports = { demo };
}