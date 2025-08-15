# :material-desktop-classic: 系统要求

## :fontawesome-solid-computer: 操作系统

| 操作系统       | 支持状态 | 最低版本要求       | 备注说明              |
|----------------|----------|--------------------|-----------------------|
| Windows        | ✅       | 7                  | 完全支持              |
| Windows        | ✅       | 8/10/11            | 最佳体验              |
| macOS          | ❌       |                    | 未来计划支持          |
| Linux          | ❌       |                    | 未来计划支持          |

!!! warning "软件版本兼容性说明"
    - **v1.0.0-beta及以上版本**：支持 Windows 7 及以上系统
    - **v1.0.0-beta以前版本**：仅支持 Windows 10 及以上系统

## :material-cpu-64-bit: 架构要求

:material-check-circle:{ .lg .middle .success } __64位系统__  :material-close-circle:{ .lg .middle .danger } __32位系统__  

???+ failure "32 位系统不支持的原因"
    1. **ttkbootstrap 版本限制**
    2. **其他依赖库兼容性问题**

    ```mermaid
    graph LR
        A[ttkbootstrap 版本限制] -->|导致| B(API 限制 & 缺少32位支持)
        D[其他依赖库兼容性问题] -->|引发| E(文件操作失败 & 依赖冲突)
        B --> G[无法运行]
        E --> G
    ```

## :material-chip: 硬件要求

| 组件       | 最低要求       | 推荐配置       | 说明                     |
|------------|----------------|----------------|--------------------------|
| :material-cpu-32-bit: 处理器 | 1 GHz 单核     | 2 GHz 双核     | 现代处理器性能更佳       |
| :material-memory: 内存      | 512 MB RAM     | 1 GB RAM       | 复杂操作需要更多内存     |
| :material-harddisk: 存储空间 | 50 MB 可用     | 100 MB 可用    | 用于程序文件和临时文件   |
| :material-monitor: 显示器    | 1024×768 分辨率 | 1920×1080 分辨率 | 更高分辨率体验更佳       |

!!! tip "提示"
    大多数现代计算机都能轻松满足这些要求。

