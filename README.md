# ADB PerfMon

一个基于 Python3 + Tkinter + ADB 的 Android APP 性能监控与自动化测试工具。

---

## 功能特性

- **CPU 使用率监控**：实时采集应用 CPU 占用率
- **内存占用监控**：监控应用内存使用情况（PSS/RSS）
- **网络流量统计**：统计应用上传/下载流量
- **APP 启动时间测试**：精确测量应用冷启动/热启动耗时
- **Monkey 压力测试**：支持与性能监控同时进行
- **可视化报告**：生成 Excel 报告和图表

---

## 技术栈

- **语言**: Python 3.x
- **UI 框架**: Tkinter
- **核心工具**: Android ADB
- **报告生成**: openpyxl, matplotlib

---

## 环境要求

- Python 3.6+
- Android SDK (ADB)
- 设备开启开发者选项和 USB 调试

### 安装依赖

```bash
pip install -r requirements.txt
```

---

## 快速开始

### 1. 配置 ADB 环境

确保 ADB 已添加到系统环境变量：

```bash
# 验证 ADB 是否配置成功
adb devices
```

### 2. 连接设备

通过 USB 连接 Android 设备，并确保设备已授权。

### 3. 启动应用

```bash
python adb_tk.py
```

---

## 使用说明

### 性能测试

1. 在主界面输入目标应用包名
2. 设置采样间隔和测试时长
3. 点击「开始监控」按钮
4. 测试结束后自动生成报告

### Monkey 测试

1. 配置 Monkey 参数（事件数、种子值）
2. 勾选「同时监控性能」选项
3. 点击「开始 Monkey 测试」
4. 测试过程中实时显示性能数据

### 启动时间测试

1. 输入目标应用包名和 Activity 名
2. 设置测试次数
3. 点击「测试启动时间」
4. 查看平均启动时间和详细日志

---

## 项目结构

```
ADB_PerfMon/
├── adb/                  # ADB 核心模块
│   ├── adb_python.py     # ADB 命令封装
│   └── checkpath.py      # 路径检查工具
├── common/               # 公共模块
│   ├── configpath.py     # 配置路径管理
│   └── generic.py        # 通用工具函数
├── config/               # 配置文件
│   ├── director.txt      # 目录配置
│   └── log.conf          # 日志配置
├── other_adb/            # 扩展功能模块
│   ├── Performance.py    # 性能监控核心
│   ├── StartTime.py      # 启动时间测试
│   ├── monkey.py         # Monkey 测试模块
│   └── android_monitor.py # Android 监控
├── utils/                # 工具模块
│   ├── handler_excel.py  # Excel 处理
│   ├── logger.py         # 日志管理
│   └── Data_Charts.py    # 数据图表生成
├── TestData/             # 测试数据目录
├── xlsxReports/          # Excel 报告输出
├── pngReports/           # 图片报告输出
├── README.md             # 项目说明
├── AGENT.md              # 代理配置说明
├── requirements.txt      # 依赖清单
└── adb_tk.py             # 主界面入口
```

---

## 注意事项

1. **线程安全**：性能数据采集采用多线程方式，避免 Tkinter 界面阻塞
2. **权限要求**：部分功能需要 root 权限（如精确流量统计）
3. **设备兼容性**：建议使用 Android 5.0 及以上版本
4. **数据准确性**：CPU 和内存数据通过 `top` 命令获取，可能存在轻微误差
5. **流量统计**：Android 10+ 版本限制了流量统计 API，可能需要特殊处理

---

## 故障排除

| 问题 | 可能原因 | 解决方案 |
|------|----------|----------|
| ADB 设备未检测 | USB 调试未开启 | 在设备上开启开发者选项和 USB 调试 |
| 权限拒绝 | 缺少必要权限 | 检查设备是否已授权或需要 root |
| 界面卡死 | 主线程阻塞 | 确保所有耗时操作在子线程中执行 |
| 流量数据异常 | Android 版本限制 | 使用其他流量统计方式或降级方案 |

---

## License

MIT License

---

## 更新日志

| 版本 | 日期 | 更新内容 |
|------|------|----------|
| 1.0.0 | 2022-05 | 初始版本，支持基础性能监控 |
