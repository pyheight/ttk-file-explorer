// 首页两个图表项竖向分割线设置
document.addEventListener('DOMContentLoaded', function() {
  function adjustDividerHeight() {
    const container = document.querySelector('.graphs-container');
    const verticalDivider = document.querySelector('.vertical-divider');
    
    if (!container || !verticalDivider) return;
    
    if (window.innerWidth >= 768) {
      // 获取两个图表项的高度
      const items = document.querySelectorAll('.graph-item');
      const heights = Array.from(items).map(item => item.offsetHeight);
      
      // 使用最大高度作为分割线高度
      const maxHeight = Math.max(...heights);
      verticalDivider.style.height = `${maxHeight}px`;
    } else {
      // 小屏幕时重置高度
      verticalDivider.style.height = '';
    }
  }
  
  // 初始调整
  adjustDividerHeight();
  
  // 窗口大小变化时调整
  window.addEventListener('resize', adjustDividerHeight);
  
  // 图片加载后重新调整
  const images = document.querySelectorAll('.graph-item img');
  images.forEach(img => {
    img.addEventListener('load', adjustDividerHeight);
  });
});
