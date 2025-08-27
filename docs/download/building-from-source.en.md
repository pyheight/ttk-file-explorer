# :material-source-branch: Building from Source

## :octicons-package-24: Cross-Platform Notes

!!! warning "Current Platform Limitations"
    ```mermaid
    graph LR
        A[tkinter GUI] --> B[Cross-platform]
        C[File Operation API] --> D[Windows-only Implementation]
        D --> E[Deep System Integration]
        E --> F[Windows API Calls]
    ```
    
    - Although tkinter is cross-platform, **the file operation API is currently implemented only for Windows**.
    - macOS/Linux builds require rewriting the file operation module.
    - The current development environment is limited to Windows, and the source code only supports Windows builds.

## :material-microsoft-windows: Windows Build Requirements

### :fontawesome-brands-python: Python Version Compatibility

| OS             | Python Version | Notes                      |
|----------------|----------------|----------------------------|
| Windows 7      | ≤ 3.8          | Last version supporting Win7 |
| Windows 8/10/11| ≥ 3.7          | Python 3.10+ recommended    |

!!! tip "Windows 7 Special Requirements"
    Due to DLL limitations in shared library linking, the last compatible Python version for Windows 7 is 3.8.

### :material-cog: System Environment Variables Configuration

!!! example "May need manual setup before packaging"
    ```python title="Key-Value Example" 
    TCL_LIBRARY: tcl_library_path
    TK_LIBRARY: tk_library_path
    ```

???+ info "Why This Is Needed"
    On some systems (e.g., Windows 7), PyInstaller may fail to locate the `init.tcl` file, causing packaging failures.

## :material-package-variant: Required Dependencies

<div class="grid cards" markdown>

- :material-web: **Web Processing**  
beautifulsoup4 · Markdown · Requests

- :material-file: **Document Processing**  
chardet · openpyxl · python_docx · python_pptx · fpdf

- :material-image: **Image Processing**  
Pillow

- :material-cog: **System Tools**  
psutil · watchdog · winshell · pywin32 · pystray · darkdetect

- :material-package: **Packaging Tools**  
pyinstaller

- :material-palette: **UI Enhancement**  
ttkbootstrap

</div>

## :material-hammer-wrench: Build Steps

1. :material-package-down: **Prerequisites**
> Ensure `Python 3.x` environment is installed

2. :material-git: **Clone or Download Repository**

    === "Clone Repository (Recommended)"
        ```bash
        git clone https://github.com/pyheight/ttk-file-explorer.git
        ```

    === "Download Repository"  
        === "Accelerated Download (Recommended)"  
            ```
            https://gh.jasonzeng.dev/https://github.com/pyheight/ttk-file-explorer/archive/refs/heads/main.zip
            ```

        === "Normal Download"  
            ```
            https://github.com/pyheight/ttk-file-explorer/archive/refs/heads/main.zip
            ```

3. :material-folder-move: **Navigate to Source Directory**
```bash
cd ttk-file-explorer/src
```

4. :material-library: **Install Dependencies**

	=== "Install Specific Versions (Recommended)"
        ```powershell
        pip install -r requirements.txt
        ```

	=== "Install Latest Versions"
        ```powershell
        pip install -r requirements_latest.txt
        ```

5. :material-play: **Launch Application**
```bash
python main.py
```

6. :material-package-variant: **Package Application**
```bash
python script/package.py
```

---

!!! bug "Encountering Issue"
	[:material-bug: Let's Solve It](../../community/issue-reporting/){ .md-button .md-button--primary }
