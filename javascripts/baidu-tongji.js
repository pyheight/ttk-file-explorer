// var _hmt = _hmt || [];
// (function() {
//   var hm = document.createElement("script");
//   hm.src = "https://hm.baidu.com/hm.js?4d7a721944e656b18e9935e354c1b44b";
//   var s = document.getElementsByTagName("script")[0]; 
//   s.parentNode.insertBefore(hm, s);
// })();

// 百度统计控制对象
window.baiduTongji = {
  // 加载统计脚本
  load: function() {
    if (typeof _hmt === "undefined") {
      window._hmt = [];
      var hm = document.createElement("script");
      hm.src = "https://hm.baidu.com/hm.js?4d7a721944e656b18e9935e354c1b44b";
      var s = document.getElementsByTagName("script")[0]; 
      s.parentNode.insertBefore(hm, s);
    }
    // 确保开启追踪（默认是开启的）
    this.enableTracking();
  },
  
  // 开启数据采集
  enableTracking: function() {
    if (typeof _hmt !== "undefined") {
      _hmt.push(['_setAutoTracking', true]);
    }
  },
  
  // 关闭数据采集
  disableTracking: function() {
    if (typeof _hmt !== "undefined") {
      _hmt.push(['_setAutoTracking', false]);
    }
  }
};
