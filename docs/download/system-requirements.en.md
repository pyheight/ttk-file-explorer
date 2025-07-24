# :material-desktop-classic: System Requirements

## :fontawesome-solid-computer: Operating System

| OS            | Support | Minimum Version    | Notes                   |
|---------------|---------|--------------------|-------------------------|
| Windows       | ✅      | 7                  | Fully supported         |
| Windows       | ✅      | 8/10/11            | Best experience         |
| macOS         | ❌      |                    | Planned for future support |
| Linux         | ❌      |                    | Planned for future support |

!!! warning "Software Version Compatibility"
    - **v1.0.0-beta and above**: Supports Windows 7 and later systems
    - **Versions before v1.0.0-beta**: Only supports Windows 10 and later systems

## :material-cpu-64-bit: Architecture Requirements

:material-check-circle:{ .lg .middle .success } __64-bit Systems__  :material-close-circle:{ .lg .middle .danger } __32-bit Systems__  

???+ failure "Reasons for not supporting 32-bit systems"
    1. **ttkbootstrap version limitations**
    2. **Compatibility issues with other dependencies**

    ```mermaid
    graph LR
        A[ttkbootstrap version limitations] -->|leads to| B(API limitations & lack of 32-bit support)
        D[Compatibility issues with other dependencies] -->|causes| E(File operation failures & dependency conflicts)
        B --> G[Unable to run]
        E --> G
    ```

## :material-chip: Hardware Requirements

| Component      | Minimum         | Recommended      | Notes                      |
|----------------|-----------------|------------------|----------------------------|
| :material-cpu-32-bit: Processor | 1 GHz single-core | 2 GHz dual-core  | Modern processors perform better |
| :material-memory: RAM      | 512 MB          | 1 GB             | Complex operations require more RAM |
| :material-harddisk: Storage | 50 MB free      | 100 MB free      | For program files and temporary storage |
| :material-monitor: Display | 1024×768 resolution | 1920×1080 resolution | Higher resolution provides better experience |

!!! tip "Tip"
    Most modern computers can easily meet these requirements.
