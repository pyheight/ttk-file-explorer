document.addEventListener('DOMContentLoaded', function() {
  // 找到所有指向 zread.ai 的导航链接
  const externalLinks = document.querySelectorAll('a[href*="zread.ai"]');
  
  externalLinks.forEach(link => {
    link.setAttribute('target', '_blank');
    link.setAttribute('rel', 'noopener noreferrer');
  });
});
