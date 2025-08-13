# :material-bug: Issue Reporting

## :material-alert: Only Latest Versions Receive Active Updates

!!! question "Encountered an issue or have a suggestion?"
    Your feedback is crucial for improving ttk file explorer!  

    **You can provide feedback through any of these methods:**

    [:material-github: GitHub Issues](https://github.com/pyheight/ttk-file-explorer/issues){ .md-button .md-button--primary }
    [:material-forum: Start Discussion](https://github.com/pyheight/ttk-file-explorer/discussions){ .md-button }
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
| :material-alert: **Critical Bug**<br><small>Crash/data loss</small> | :material-star: :material-star: :material-star: :material-star: :material-star: | [:material-github: GitHub Issues](https://github.com/pyheight/ttk-file-explorer/issues) |
| :material-feature-search: **Feature Request**<br><small>New feature/improvement suggestion</small> | :material-star: :material-star: :material-star: :material-star: | [:material-forum: Start Discussion](https://github.com/pyheight/ttk-file-explorer/discussions) or [:material-comment: Comment Here](#giscus-comments)  |
| :material-help-box: **Usage Question**<br><small>Configuration/operation guidance</small> | :material-star: :material-star: :material-star: | [:material-forum: Start Discussion](https://github.com/pyheight/ttk-file-explorer/discussions) or [:material-comment: Comment Here](#giscus-comments) |

!!! tip "Tip"
    :material-clock: We'll address reports as soon as possible. Thank you for your patience and support!

## :material-check-all: Pre-submission Checklist

- [x] Searched [existing issues](https://github.com/pyheight/ttk-file-explorer/issues)
- [x] Included necessary environment information
- [ ] Provided clear reproduction steps

---

## :material-comment: <span id="giscus-comments">Comment Here</span> { #giscus-comments }

<small>You can submit feedback or suggestions directly on this page</small>

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
        script.setAttribute('data-lang', 'en');
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
