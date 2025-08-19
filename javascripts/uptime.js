document.addEventListener("DOMContentLoaded", function() {
  const launchDate = new Date("2025-07-24T00:00:00");
  
  function formatRuntime(days, hours, minutes, seconds) {
    return `${days}d ${hours}h ${minutes}m ${seconds}s`;
  }
  
  // 更新运行时间显示的函数
  function updateRuntime() {
    const now = new Date();
    const diff = Math.abs(now - launchDate);
    
    // 计算时间单位
    const days = Math.floor(diff / (1000 * 60 * 60 * 24));
    const hours = Math.floor((diff % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
    const minutes = Math.floor((diff % (1000 * 60 * 60)) / (1000 * 60));
    const seconds = Math.floor((diff % (1000 * 60)) / 1000);
    
    // 获取显示元素并更新内容
    const runtimeElement = document.getElementById("site-runtime");
    if (runtimeElement) {
      runtimeElement.textContent = formatRuntime(days, hours, minutes, seconds);
    }
  }
  
  // 初始更新
  updateRuntime();
  
  // 每秒更新一次
  setInterval(updateRuntime, 1000);
});
