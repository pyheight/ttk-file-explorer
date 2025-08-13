# :material-bug: Issue Reporting

## :material-alert: Only Latest Versions Receive Active Updates

!!! question "Encountered an issue or have a suggestion?"
    Your feedback is crucial for improving ttk file explorer!  

    **You can provide feedback through any of these methods:**

    [:material-github: GitHub Issues](https://github.com/pyheight/ttk-file-explorer/issues){ .md-button .md-button--primary  target="_blank"}
    [:material-forum: Start Discussion](https://github.com/pyheight/ttk-file-explorer/discussions){ .md-button  target="_blank"}
    [:material-email: Email](mailto:pyheight@qq.com){ .md-button }
    [:material-comment: Comment Here](#giscus-comments){ .md-button }

## :material-file-document: Reporting Requirements

!!! info "Please provide the following information"
    1. **Issue Description**  
    Problem encountered · Frequency and conditions of occurrence

    2. **Reproduction Steps**  
    Step 1 · Step 2 · Observed result

    3. **Environment Information**  
    OS version · Software version

    4. **Additional Information**  
    Screenshots or screen recordings · Error logs (if available) · Contact details (optional)

## :material-help-circle: Reporting Guidelines

| Report Type | Priority | Recommended Channel |
|-------------|----------|---------------------|
| :material-alert: **Critical Bug**<br><small>Crash/data loss</small> | :material-star: :material-star: :material-star: :material-star: :material-star: | [:material-github: GitHub Issues](https://github.com/pyheight/ttk-file-explorer/issues){ target="_blank" } |
| :material-feature-search: **Feature Request**<br><small>New feature/improvement suggestion</small> | :material-star: :material-star: :material-star: :material-star: | [:material-forum: Start Discussion](https://github.com/pyheight/ttk-file-explorer/discussions){ target="_blank" } or [:material-comment: Comment Here](#giscus-comments) |
| :material-help-box: **Usage Question**<br><small>Configuration/operation guidance</small> | :material-star: :material-star: :material-star: | [:material-forum: Start Discussion](https://github.com/pyheight/ttk-file-explorer/discussions){ target="_blank" } or [:material-comment: Comment Here](#giscus-comments) |

!!! tip "Tip"
    :material-clock: We'll address reports as soon as possible. Thank you for your patience and support!

## :material-check-all: Pre-submission Checklist

- [x] Searched [existing issues](https://github.com/pyheight/ttk-file-explorer/issues){ target="_blank" }
- [x] Included necessary environment information
- [ ] Provided clear reproduction steps

---

## :material-comment: <span id="giscus-comments">Comment Here</span> { #giscus-comments }

<small>You can submit feedback or suggestions directly on this page</small>

<div class="giscus"></div>
<script>
  document.addEventListener('DOMContentLoaded', function() {
    // 创建Giscus脚本元素
    const giscusScript = document.createElement('script');
    giscusScript.src = 'https://giscus.app/client.js';
    giscusScript.setAttribute('data-repo', 'pyheight/ttk-file-explorer');
    giscusScript.setAttribute('data-repo-id', 'R_kgDOKsdh1g');
    giscusScript.setAttribute('data-category', 'General');
    giscusScript.setAttribute('data-category-id', 'DIC_kwDOKsdh1s4CbYu7');
    giscusScript.setAttribute('data-mapping', 'pathname');
    giscusScript.setAttribute('data-strict', '0');
    giscusScript.setAttribute('data-reactions-enabled', '1');
    giscusScript.setAttribute('data-emit-metadata', '1');
    giscusScript.setAttribute('data-input-position', 'top');
    giscusScript.setAttribute('data-lang', 'en');
    giscusScript.setAttribute('data-loading', 'lazy');
    giscusScript.crossOrigin = 'anonymous';
    giscusScript.async = true;
    
    // 获取当前主题
    function getGiscusTheme() {
      const palette = __md_get('__palette');
      if (palette && typeof palette.color === 'object') {
        // 深色模式使用 noborder_gray，浅色模式使用 noborder_light
        return palette.color.scheme === 'slate' ? 'noborder_gray' : 'noborder_light';
      }
      // 默认主题为 noborder_light
      return 'noborder_light';
    }
    
    // 初始设置主题
    giscusScript.setAttribute('data-theme', getGiscusTheme());
    
    // 添加到页面
    const giscusContainer = document.querySelector('.giscus');
    giscusContainer.appendChild(giscusScript);
    
    // 监听主题切换事件
    const paletteComponent = document.querySelector('[data-md-component="palette"]');
    if (paletteComponent) {
      paletteComponent.addEventListener('change', function() {
        const newTheme = getGiscusTheme();
        const giscusFrame = document.querySelector('.giscus-frame');
        
        if (giscusFrame) {
          // 更新Giscus主题
          giscusFrame.contentWindow.postMessage(
            { giscus: { setConfig: { theme: newTheme } } },
            'https://giscus.app'
          );
        }
      });
    }
    
    // 锚点跳转处理
    if (window.location.hash === '#giscus-comments') {
      setTimeout(() => {
        giscusContainer.scrollIntoView({ behavior: 'smooth' });
      }, 500);
    }
  });
</script>
