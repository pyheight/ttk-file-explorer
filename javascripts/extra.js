document.addEventListener('DOMContentLoaded', function() {
  // 标记JS已加载
  document.body.classList.add('js-loaded');
  
  // 获取相关元素
  const header = document.querySelector('.md-header');
  
  // 如果缺少关键元素则退出
  if (!header) return;
  
  const banner = document.querySelector('.md-banner');
  const tabs = document.querySelector('.md-tabs');
  
  // 创建容器元素（只包含导航栏）
  const navContainer = document.createElement('div');
  navContainer.className = 'nav-container';
  
  // 移动导航栏到容器中
  if (tabs && tabs.parentNode) {
    navContainer.appendChild(tabs);
  }
  
  // 将容器插入到标题栏后面
  header.parentNode.insertBefore(navContainer, header.nextSibling);
  
  // 初始化通知栏高度
  const updateBannerHeight = () => {
    const bannerHeight = banner && banner.offsetHeight > 0 ? banner.offsetHeight : 0;
    document.documentElement.style.setProperty('--banner-height', `${bannerHeight}px`);
    return bannerHeight;
  };
  
  let bannerHeight = updateBannerHeight();
  
  // 初始状态
  const topThreshold = 10;
  let hasAnimated = false; // 标记是否已经执行过动画
  
  // 设置初始状态函数
  const setInitialState = () => {
    // 更新通知栏高度（可能已变化）
    bannerHeight = updateBannerHeight();
    
    if (window.scrollY > topThreshold) {
      navContainer.classList.add('nav-container--hidden');
    } else {
      navContainer.classList.remove('nav-container--hidden');
      // 初始显示时触发动画（仅一次）
      if (!hasAnimated) {
        animateNavItems();
        hasAnimated = true;
      }
    }
  };
  
  setInitialState();
  
  // 滚动事件处理
  let lastScrollY = window.scrollY;
  let ticking = false;
  
  const handleScroll = () => {
    const currentScrollY = window.scrollY;
    
    // 滚动到顶部时显示
    if (currentScrollY <= topThreshold) {
      navContainer.classList.remove('nav-container--hidden');
    } 
    // 向下滚动时隐藏
    else if (currentScrollY > lastScrollY && currentScrollY > topThreshold) {
      navContainer.classList.add('nav-container--hidden');
    }
    
    lastScrollY = currentScrollY;
    ticking = false;
  };
  
  window.addEventListener('scroll', () => {
    if (!ticking) {
      window.requestAnimationFrame(handleScroll);
      ticking = true;
    }
  });
  
  // 导航栏标签滑动动画函数（优化版）
  function animateNavItems() {
    const tabItems = document.querySelectorAll('.md-tabs__item:not(.animated)');
    
    tabItems.forEach((item, index) => {
      // 添加标记避免重复动画
      item.classList.add('animated');
      
      // 设置延迟动画（使用transition而非animation）
      setTimeout(() => {
        item.classList.add('animate-in');
      }, index * 80); // 增加延迟时间
    });
  }
  
  // 监听通知栏关闭事件
  if (banner) {
    // 关闭按钮点击事件
    const closeButton = banner.querySelector('.md-banner__close');
    if (closeButton) {
      closeButton.addEventListener('click', () => {
        // 添加翻转关闭动画
        banner.classList.remove('flip-in');
        banner.classList.add('flip-out');
        
        // 等待动画完成后更新高度
        setTimeout(() => {
          bannerHeight = 0;
          document.documentElement.style.setProperty('--banner-height', '0px');
          
          // 更新导航容器位置
          navContainer.style.top = '2.4rem';
          
          // 更新内容区域上边距
          document.querySelectorAll('.md-main').forEach(el => {
            el.style.marginTop = '2.4rem';
          });
        }, 600);
      });
    }
    
    // 监听Material原生的通知栏隐藏事件
    banner.addEventListener('animationend', (e) => {
      if (e.animationName.includes('flipOut') || e.animationName.includes('flip-out')) {
        bannerHeight = 0;
        document.documentElement.style.setProperty('--banner-height', '0px');
        navContainer.style.top = '2.4rem';
      }
    });
  }
  
  // 响应窗口大小变化
  const resizeObserver = new ResizeObserver(() => {
    const newBannerHeight = updateBannerHeight();
    if (newBannerHeight !== bannerHeight) {
      bannerHeight = newBannerHeight;
      navContainer.style.top = `calc(2.4rem + ${bannerHeight}px)`;
    }
  });
  
  if (banner) {
    resizeObserver.observe(banner);
  }
  
  // 添加导航栏标签点击效果 - 涟漪
  const tabLinks = document.querySelectorAll('.md-tabs__link');
  tabLinks.forEach(link => {
    link.addEventListener('click', (e) => {
      // 添加点击涟漪效果
      createRippleEffect(e, link);
    });
  });
  
  // 创建涟漪效果函数
  function createRippleEffect(event, element) {
    // 移除现有的涟漪效果
    const existingRipples = element.querySelectorAll('.ripple-effect');
    existingRipples.forEach(ripple => ripple.remove());
    
    // 创建新的涟漪元素
    const ripple = document.createElement('span');
    ripple.classList.add('ripple-effect');
    
    // 计算位置和大小
    const rect = element.getBoundingClientRect();
    const size = Math.max(rect.width, rect.height);
    const x = event.clientX - rect.left - size / 2;
    const y = event.clientY - rect.top - size / 2;
    
    // 设置样式
    ripple.style.width = ripple.style.height = `${size}px`;
    ripple.style.left = `${x}px`;
    ripple.style.top = `${y}px`;
    
    // 添加到元素
    element.appendChild(ripple);
    
    // 设置动画结束后移除
    setTimeout(() => {
      ripple.remove();
    }, 600);
  }
});


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


//雪花特效
const fps = 30;
const mspf = Math.floor(1000 / fps) ; 

let width = window.innerWidth || document.documentElement.clientWidth;
let height = window.innerHeight || document.documentElement.clientHeight;
let canvas;
window.addEventListener('resize', () => {
  width = window.innerWidth || document.documentElement.clientWidth;
  height = window.innerHeight || document.documentElement.clientHeight;
  if (canvas) {
    canvas.width = width;
    canvas.height = height;
  }
});

let particles = [];
let wind = [0, 0];
let cursor = [0, 0];

function velocity(r) {
  return 70 / r + 30;
  }

  function sine_component(h, a) {
    return [2 * Math.PI / h, Math.random() * a, Math.random() * 2 * Math.PI]; // [frequency, amplitude, phase]
  }

  function calc_sine(components, x) {
    let sum = 0;
    for (let i = 0; i < components.length; i++) {
      const [f, a, p] = components[i];
      sum += Math.sin(x * f + p) * a;
    }
    return sum;
  }

  function gen_particle() {
    let r = Math.random() * 4 + 1;
    return {
      radius: r,
        x: Math.random() * width,
        y: -r,
    opacity: Math.random(),
    sine_components: [sine_component(height, 3), sine_component(height / 2, 2), sine_component(height / 5, 1), sine_component(height / 10, 0.5)],
    };
    }

    function update_pos(dt) {
      const n = particles.length;
      for (let i = 0; i < n; i++) {
        const v = velocity(particles[i].radius);
        particles[i].x += calc_sine(particles[i].sine_components, particles[i].y) * v / 5 * dt;
        particles[i].y += v * dt;

        // const dist = Math.hypot(particles[i].x - cursor[0], particles[i].y - cursor[1]) + 1;
        // particles[i].x += wind[0] * dt / dist
        // particles[i].y += wind[1] * dt / dist;

        if (particles[i].y - particles[i].radius > height) {
          particles[i] = gen_particle();  
        }
      }
    }

    let context_cache;
    function get_context() {
      if (context_cache)
      return context_cache;

      canvas = document.createElement('canvas');
      canvas.id = 'snow-canvas';
      canvas.width = width;
      canvas.height = height;
      canvas.style = 'position: fixed; top: 0; left: 0; overflow: hidden; pointer-events: none; z-index: 256;';
      if ((document.documentElement.dataset.darkreaderMode || "").startsWith('filter'))
      canvas.style.filter = 'invert(1)';
      document.body.appendChild(canvas);

      context_cache = canvas.getContext('2d');
      return context_cache;
    }

    function draw() {
      const ctx = get_context();

      ctx.clearRect(0, 0, width, height);

      const n = particles.length;
      for (let i = 0; i < n; i++) {
        const p = particles[i];
        ctx.fillStyle = `rgba(255, 255, 255, ${p.opacity})`;
        ctx.shadowColor = '#80EDF7';
        ctx.shadowBlur = 7;
        ctx.beginPath();
        ctx.arc(p.x, p.y, p.radius, 0, 2*Math.PI);
        ctx.fill();
        }
        }

        let focused = true;
        let disabled = false;
        let lastTime = performance.now();
        const requestFrame = () => setTimeout(loop, mspf);
        function loop() {
          const dt = (performance.now() - lastTime) / 1000;

          if (particles.length < 120 && Math.random() < 0.1) {
          particles.push(gen_particle());
  }
  
  update_pos(dt);
  draw();
  
  lastTime = performance.now();
  if (focused && !disabled)
    requestFrame();
}


window.addEventListener('focus', () => {
  console.log('snow start');
  focused = true;
  lastTime = performance.now();
  requestFrame();
});

window.addEventListener('blur', () => {
  console.log('snow stop');
  focused = false;
});

window.addEventListener('keydown', e => {
  if (e.ctrlKey && e.key == 's') {
    e.preventDefault();
    disabled = !disabled;
    if (disabled) {
      canvas.style.display = 'none';
    } else {
      canvas.style.display = 'block';
      lastTime = performance.now();
      requestFrame();
    }
  }
});

requestFrame();
