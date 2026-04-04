# 🤖 自动化脚本示例 | Automation Script Examples

本目录包含各种自动化任务的使用示例。

---

## 📚 示例列表

### 1. 文件批量处理
自动重命名、移动、备份文件。

**使用命令**:
```
将 photos 目录下的所有图片按日期重命名
```

**功能**:
- 批量重命名文件
- 按规则整理目录
- 自动备份重要文件
- 清理临时文件

### 2. 系统监控脚本
监控系统资源和使用情况。

**使用命令**:
```
创建一个系统监控脚本，每 5 分钟记录 CPU 和内存使用率
```

**监控内容**:
- CPU 使用率
- 内存占用
- 磁盘空间
- 网络流量
- 进程状态

### 3. 定时任务管理
创建和管理定时执行的任务。

**使用命令**:
```
设置每天凌晨 2 点自动备份数据库
```

**实现方式**:
- Windows 任务计划程序
- Linux cron job
- Python schedule 库
- systemd timers

### 4. 邮件通知
发送自动化通知邮件。

**使用命令**:
```
创建邮件通知服务，当磁盘空间不足 10% 时报警
```

**支持**:
- SMTP 邮件发送
- HTML 格式邮件
- 附件支持
- 邮件模板

---

## 💡 使用技巧

### 1. 文件操作
```
# 批量重命名
"将所有 .txt 文件重命名为 .md"

# 按类型分类
"将下载文件夹中的文件按扩展名分类到不同目录"
```

### 2. 系统维护
```
# 日志清理
"删除 30 天前的日志文件"

# 磁盘清理
"查找并删除大于 100MB 的临时文件"
```

### 3. 网络操作
```
# 批量下载
"从 URL 列表批量下载图片"

# 网站监控
"检查网站是否正常访问，失败时发送通知"
```

---

## 🔧 相关工具

衍智体提供以下自动化工具：

| 工具名称 | 功能描述 |
|---------|---------|
| `bash` | 执行 Bash 命令 |
| `powershell` | 执行 PowerShell 命令 |
| `file_read` | 读取文件 |
| `file_write` | 写入文件 |
| `task_create` | 创建定时任务 |

---

## 📖 实用脚本模板

### 文件备份脚本

```python
"""
自动备份脚本 - 定期备份重要目录
"""

import shutil
from datetime import datetime
from pathlib import Path

def backup_directory(source: Path, dest: Path) -> None:
    """备份目录"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_name = f"backup_{timestamp}"
    backup_path = dest / backup_name

    print(f"正在备份 {source} 到 {backup_path}")
    shutil.copytree(source, backup_path)
    print("✅ 备份完成")

if __name__ == "__main__":
    source_dir = Path("/path/to/important/data")
    backup_dest = Path("/path/to/backups")
    backup_directory(source_dir, backup_dest)
```

### 系统监控脚本

```python
"""
系统资源监控 - 记录资源使用情况
"""

import psutil
import time
from datetime import datetime

def monitor_system(interval: int = 300) -> None:
    """监控系统资源"""
    while True:
        # 获取系统信息
        cpu_percent = psutil.cpu_percent(interval=1)
        memory = psutil.virtual_memory()
        disk = psutil.disk_usage('/')

        # 记录日志
        timestamp = datetime.now().isoformat()
        log_line = (
            f"{timestamp} | "
            f"CPU: {cpu_percent}% | "
            f"Memory: {memory.percent}% | "
            f"Disk: {disk.percent}%\n"
        )

        with open("system_monitor.log", "a") as f:
            f.write(log_line)

        print(f"[{timestamp}] CPU: {cpu_percent}%, Memory: {memory.percent}%")

        time.sleep(interval)

if __name__ == "__main__":
    monitor_system()
```

### 邮件通知脚本

```python
"""
邮件通知服务 - 发送告警邮件
"""

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_alert(
    subject: str,
    message: str,
    to_email: str,
    smtp_server: str = "smtp.gmail.com",
    smtp_port: int = 587
) -> None:
    """发送告警邮件"""
    msg = MIMEMultipart()
    msg['From'] = 'your-email@gmail.com'
    msg['To'] = to_email
    msg['Subject'] = f"[ALERT] {subject}"

    msg.attach(MIMEText(message, 'html'))

    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login('your-email@gmail.com', 'password')
        server.send_message(msg)
        print(f"✅ 邮件已发送至 {to_email}")

if __name__ == "__main__":
    send_alert(
        subject="磁盘空间不足",
        message="<h1>警告</h1><p>磁盘使用率超过 90%</p>",
        to_email="admin@example.com"
    )
```

---

## 🎯 实战案例

### 案例 1: 项目部署自动化

```bash
# 步骤 1: 代码更新
yzt "编写脚本：从 Git 拉取最新代码"

# 步骤 2: 依赖安装
yzt "添加自动安装 pip 依赖的功能"

# 步骤 3: 服务重启
yzt "添加重启 Nginx 和 Gunicorn 的命令"

# 步骤 4: 健康检查
yzt "添加部署后健康检查，失败时回滚"
```

### 案例 2: 数据同步

```bash
# 步骤 1: 数据导出
yzt "从数据库导出数据为 CSV"

# 步骤 2: 数据转换
yzt "转换数据格式以匹配目标系统"

# 步骤 3: 数据导入
yzt "导入数据到目标数据库"

# 步骤 4: 验证
yzt "验证数据一致性，生成报告"
```

---

## ⚠️ 注意事项

### 安全建议
- ✅ 不要在脚本中硬编码密码
- ✅ 使用环境变量或配置文件
- ✅ 对用户输入进行验证
- ✅ 设置适当的文件权限
- ✅ 记录所有操作日志

### 错误处理
```python
try:
    # 可能出错的操作
    result = risky_operation()
except Exception as e:
    # 记录错误
    logger.error(f"操作失败: {e}")
    # 发送通知
    send_alert("操作失败", str(e))
    # 优雅退出
    sys.exit(1)
```

---

**继续探索更多示例！**

[返回上级](../README.md) | [数据处理](../data_processing/README.md) | [API 集成](../api_integration/README.md)
