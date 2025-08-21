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

// 监听语言切换事件
document$.subscribe(function() {
  // 获取当前语言
  const lang = document.documentElement.lang || 'zh';
  
  // 更新 Cookie 同意表单描述
  updateConsentDescription(lang);
  
  // 监听语言切换按钮点击
  document.querySelectorAll('a[href^="/ttk-file-explorer/en/"], a[href^="/ttk-file-explorer/"]').forEach(link => {
    link.addEventListener('click', () => {
      // 添加延迟确保语言切换完成
      setTimeout(() => {
        const newLang = link.getAttribute('href').includes('/en/') ? 'en' : 'zh';
        updateConsentDescription(newLang);
      }, 100);
    });
  });
});

// 更新描述内容的函数
function updateConsentDescription(lang) {
  const zhDesc = document.getElementById('consent-description-zh');
  const enDesc = document.getElementById('consent-description-en');
  
  if (zhDesc && enDesc) {
    zhDesc.style.display = lang === 'zh' ? 'block' : 'none';
    enDesc.style.display = lang === 'en' ? 'block' : 'none';
  }

  const title = document.querySelector('.md-consent__title');
  if (title) {
    null
  }
}

// 初始化
document.addEventListener('DOMContentLoaded', () => {
  const lang = document.documentElement.lang || 'zh';
  updateConsentDescription(lang);
});
