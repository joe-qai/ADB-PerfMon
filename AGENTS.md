### ADB_Monkey_Performance 代理配置说明

---

#### 1. 项目概述
本项目是一个基于 Python3 + Tkinter + ADB 的 Android APP 性能监控工具，支持以下功能：
- CPU 使用率监控
- 内存占用监控
- 网络流量统计（上传/下载）
- APP 启动时间测试
- Monkey 压力测试（与性能测试同时进行）

---

#### 2. 代理配置

##### 2.1 ADB 环境要求
- **环境变量配置**：确保系统已配置 ADB 环境变量
- **设备连接**：通过 USB 或网络连接 Android 设备
- **权限要求**：设备需开启开发者选项并允许 USB 调试

##### 2.2 网络代理设置（可选）
如需通过代理访问网络，可在测试前配置：

```bash
# 设置全局代理
adb shell settings put global http_proxy <proxy_host>:<proxy_port>

# 取消代理
adb shell settings put global http_proxy :0
```

---

#### 3. 目录结构说明

```
Adb_Monkey_Performance/
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
└── adb_tk.py             # 主界面入口
```

---

#### 4. 代理执行流程

##### 4.1 启动流程
```
1. 检查 ADB 环境变量
2. 检测连接设备
3. 加载配置文件
4. 启动 Tkinter 界面
5. 等待用户操作
```

##### 4.2 性能测试流程
```
1. 选择目标 APP（包名）
2. 设置测试参数（采样间隔、时长）
3. 启动监控线程
4. 实时采集数据（CPU/内存/流量）
5. 生成测试报告
```

##### 4.3 Monkey 测试流程
```
1. 配置 Monkey 参数（事件数、种子、包名限制）
2. 启动 Monkey 测试
3. 同时开启性能监控
4. 测试结束后生成综合报告
```

---

#### 5. 配置文件说明

##### 5.1 config/director.txt
```
# 报告输出目录配置
report_dir=xlsxReports/
chart_dir=pngReports/
data_dir=TestData/
```

##### 5.2 config/log.conf
```
# 日志配置
[loggers]
keys=root,app

[handlers]
keys=consoleHandler,fileHandler

[formatters]
keys=simpleFormatter

[logger_root]
level=INFO
handlers=consoleHandler,fileHandler

[logger_app]
level=DEBUG
handlers=fileHandler
qualname=app

[handler_consoleHandler]
class=StreamHandler
level=INFO
formatter=simpleFormatter

[handler_fileHandler]
class=FileHandler
level=DEBUG
formatter=simpleFormatter
args=('app.log',)

[formatter_simpleFormatter]
format=%(asctime)s - %(name)s - %(levelname)s - %(message)s
```

---

#### 6. 代理使用示例

##### 6.1 启动主程序
```bash
python adb_tk.py
```

##### 6.2 命令行模式（待扩展）
```bash
# 性能测试
python -m other_adb.Performance --package com.example.app --duration 60

# 启动时间测试
python -m other_adb.StartTime --package com.example.app --count 10

# Monkey 测试
python -m other_adb.monkey --package com.example.app --events 10000
```

---

#### 7. 注意事项

1. **线程安全**：性能数据采集采用多线程方式，避免 Tkinter 界面阻塞
2. **权限要求**：部分功能需要 root 权限（如精确流量统计）
3. **设备兼容性**：建议使用 Android 5.0 及以上版本
4. **数据准确性**：CPU 和内存数据通过 `top` 命令获取，可能存在轻微误差
5. **流量统计**：Android 10+ 版本限制了流量统计 API，可能需要特殊处理

---

#### 8. 故障排除

| 问题 | 可能原因 | 解决方案 |
|------|----------|----------|
| ADB 设备未检测 | USB 调试未开启 | 在设备上开启开发者选项和 USB 调试 |
| 权限拒绝 | 缺少必要权限 | 检查设备是否已授权或需要 root |
| 界面卡死 | 主线程阻塞 | 确保所有耗时操作在子线程中执行 |
| 流量数据异常 | Android 版本限制 | 使用其他流量统计方式或降级方案 |

---

#### 9. 更新日志

| 版本 | 日期 | 更新内容 |
|------|------|----------|
| 1.0.0 | 2022-05 | 初始版本，支持基础性能监控 |
