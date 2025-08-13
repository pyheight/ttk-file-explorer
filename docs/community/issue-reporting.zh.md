# :material-bug: 问题反馈

## :material-alert: 仅最新版本会积极接收更新

!!! question "遇到问题或有建议"
    您的反馈很重要，帮助我们改进 ttk file explorer！  

    **您可以选择以下任一方式反馈：**

    [:material-github: GitHub Issues](https://github.com/pyheight/ttk-file-explorer/issues){ .md-button .md-button--primary }
    [:material-forum: 发起讨论](https://github.com/pyheight/ttk-file-explorer/discussions){ .md-button }
    [:material-email: 电子邮件](mailto:pyheight@qq.com){ .md-button }
    [:material-comment: 在此评论反馈](#giscus-comments){ .md-button }

## :material-file-document: 报告要求

!!! info "请提供以下信息"
    1. **问题描述**  
    遇到的问题 · 发生频率和条件

    2. **重现步骤**  
    第一步操作 · 第二步操作 · 观察到的结果

    3. **环境信息**  
    操作系统版本 · 软件版本

    4. **附加信息**  
    截图或屏幕录制 · 错误日志（如有） · 联系方式（可选）

## :material-help-circle: 报告指南

| 报告类型 | 处理优先级 | 建议提交渠道 |
|----------|------------|--------------|
| :material-alert: **严重错误**<br><small>程序崩溃/数据丢失</small> | :material-star: :material-star: :material-star: :material-star: :material-star: | [:material-github: GitHub Issues](https://github.com/pyheight/ttk-file-explorer/issues) |
| :material-feature-search: **功能请求**<br><small>新功能/改进建议</small> | :material-star: :material-star: :material-star: :material-star: | [:material-forum: 发起讨论](https://github.com/pyheight/ttk-file-explorer/discussions) 或 [:material-comment: 在此评论反馈](#giscus-comments)  |
| :material-help-box: **使用问题**<br><small>配置/操作指导</small> | :material-star: :material-star: :material-star: | [:material-forum: 发起讨论](https://github.com/pyheight/ttk-file-explorer/discussions) 或 [:material-comment: 在此评论反馈](#giscus-comments) |

!!! tip "提示"
    :material-clock: 我们会在收到报告后尽快处理，感谢您的耐心与支持！

## :material-check-all: 提交前检查

- [x] 已搜索[现有问题](https://github.com/pyheight/ttk-file-explorer/issues)
- [x] 包含必要环境信息
- [ ] 提供清晰的重现步骤

---

## :material-comment: <span id="giscus-comments">在此评论反馈</span> { #giscus-comments }

<small>您可以直接在此页面提交问题反馈或建议</small>

<div class="giscus"></div>
<script>
  document.addEventListener('DOMContentLoaded', function() {
    const giscusContainer = document.querySelector('.giscus');
    const observer = new IntersectionObserver((entries) => {
      if (entries[0].isIntersecting) {
        const script = document.createElement('script');
        script.src = 'https://giscus.app/client.js';
        script.setAttribute('data-repo', 'pyheight/ttk-file-explorer');
        script.setAttribute('data-repo-id', 'R_kgDOKsdh1g');
        script.setAttribute('data-category', 'General');
        script.setAttribute('data-category-id', 'DIC_kwDOKsdh1s4CbYu7');
        script.setAttribute('data-mapping', 'pathname');
        script.setAttribute('data-strict', '0');
        script.setAttribute('data-reactions-enabled', '1');
        script.setAttribute('data-emit-metadata', '1');
        script.setAttribute('data-input-position', 'top');
        script.setAttribute('data-theme', 'dark_dimmed');
        script.setAttribute('data-lang', 'zh-CN');
        script.setAttribute('data-loading', 'lazy');
        script.crossOrigin = 'anonymous';
        script.async = true;
        giscusContainer.appendChild(script);
        observer.disconnect();
      }
    });
    observer.observe(giscusContainer);
    if (window.location.hash === '#giscus-comments') {
      setTimeout(() => {
        giscusContainer.scrollIntoView({ behavior: 'smooth' });
      }, 500);
    }
  });
</script>
