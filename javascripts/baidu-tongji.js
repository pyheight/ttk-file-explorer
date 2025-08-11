// var _hmt = _hmt || [];
// (function() {
//   var hm = document.createElement("script");
//   hm.src = "https://hm.baidu.com/hm.js?4d7a721944e656b18e9935e354c1b44b";
//   var s = document.getElementsByTagName("script")[0]; 
//   s.parentNode.insertBefore(hm, s);
// })();

// 百度统计条件加载函数
function loadBaiduTongji() {
  // 初始化统计队列
  window._hmt = window._hmt || [];
  
  // 创建并加载脚本
  var hm = document.createElement("script");
  hm.src = "https://hm.baidu.com/hm.js?4d7a721944e656b18e9935e354c1b44b";
  var s = document.getElementsByTagName("script")[0]; 
  s.parentNode.insertBefore(hm, s);
  
  // 启用数据采集（默认状态）
  _hmt.push(['_setAutoTracking', true]);
}

// 暴露函数给全局
window.loadBaiduTongji = loadBaiduTongji;

// 页面加载时检查用户同意状态
document$.subscribe(function() {
  // 获取当前同意状态
  const consent = __md_get("__consent");
  
  // 如果用户之前已同意analytics，自动加载统计
  if (consent && consent.analytics) {
    loadBaiduTongji();
  }
  
  // 如果用户之前拒绝，禁用数据采集
  if (consent && !consent.analytics) {
    window._hmt = window._hmt || [];
    _hmt.push(['_setAutoTracking', false]);
  }
});
