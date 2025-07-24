# :material-source-branch: 从源代码构建

## :octicons-package-24: 跨平台说明

!!! warning "当前平台限制"
    ```mermaid
    graph LR
        A[tkinter GUI] --> B[跨平台]
        C[文件操作 API] --> D[仅 Windows 实现]
        D --> E[深度系统集成]
        E --> F[Windows API 调用]
    ```
    
    - tkinter 虽然是跨平台的，但**文件操作 API 目前仅针对 Windows 实现**。
    - macOS/Linux 构建需要重写文件操作模块。
    - 当前开发环境限定在 Windows，源代码仅支持 Windows 构建。

## :material-microsoft-windows: Windows 构建要求

### :fontawesome-brands-python: Python 版本兼容性

| 操作系统       | Python 版本要求 | 说明                     |
|----------------|-----------------|--------------------------|
| Windows 7      | ≤ 3.8           | 最后一个支持 Win7 的版本 |
| Windows 8/10/11| ≥ 3.7           | 推荐使用 Python 3.10+    |

!!! tip "Windows 7 特殊要求"
    由于共享库链接的 DLL 限制，Windows 7 最后一个兼容版本是 Python 3.8。

### :material-cog: 系统环境变量配置

!!! example "在打包前可能需手动设置"
    ```python title="键对值示例" 
    TCL_LIBRARY: tcl_library_path
    TK_LIBRARY: tk_library_path
    ```

???+ info "为什么需要这个"
    在某些系统（如 Windows 7）上，PyInstaller 可能无法找到`init.tcl`文件，导致打包失败。

## :material-package-variant: 所需依赖

<div class="grid cards" markdown>

- :material-web: **网页处理**  
beautifulsoup4 · Markdown · Requests

- :material-file: **文档处理**  
chardet · openpyxl · python_docx · python_pptx · fpdf

- :material-image: **图像处理**  
Pillow

- :material-cog: **系统工具**  
psutil · watchdog · winshell · pywin32 · pystray · darkdetect

- :material-package: **打包工具**  
pyinstaller

- :material-palette: **界面美化**  
ttkbootstrap

</div>

## :material-hammer-wrench: 构建步骤

1. :material-package-down: **前置条件**  
> 确保已经安装了`Python 3.x`环境

2. :material-git: **下载或克隆仓库**
```bash
git clone https://github.com/pyheight/ttk-file-explorer.git
```

3. :material-folder-move: **导航到源码目录**
```bash
cd ttk-file-explorer/src
```

4. :material-library: **安装依赖**  

    === "安装指定版本（推荐）"  
        ```powershell
        pip install -r requirements.txt
        ```

    === "安装最新版本"  
        ```powershell
        pip install -r requirements_latest.txt
        ```

5. :material-play: **启动应用**
```bash
python main.py
```

6. :material-package-variant: **打包应用**
```bash
python script/package.py
```

---

!!! bug "遇到问题"
    [:material-bug: 让我们来解决它](../../community/issue-reporting/){ .md-button .md-button--primary }
