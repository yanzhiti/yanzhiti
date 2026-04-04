# 📊 数据处理示例 | Data Processing Examples

本目录包含数据处理和分析相关的使用示例。

---

## 📚 示例列表

### 1. CSV 文件处理
读取、处理和写入 CSV 数据。

**使用命令**:
```
帮我处理 sales.csv 文件，计算每个产品的总销售额
```

**功能**:
- 读取大型 CSV 文件
- 数据清洗和转换
- 聚合计算
- 生成报告

### 2. JSON 数据操作
处理复杂的 JSON 数据结构。

**使用命令**:
```
解析 API 返回的 JSON 数据，提取用户信息
```

**示例代码**:
```python
import json
from pathlib import Path

# 读取 JSON 文件
data = Path("users.json").read_text()
users = json.loads(data)

# 提取特定字段
user_info = [
    {
        "name": user["name"],
        "email": user["email"],
        "age": user["age"]
    }
    for user in users if user["active"]
]
```

### 3. Excel 文件操作
读写 Excel 电子表格。

**使用命令**:
```
从 data.xlsx 读取数据，生成统计图表
```

**依赖库**: pandas, openpyxl

### 4. 数据库操作
与各种数据库交互。

**使用命令**:
```
连接 PostgreSQL 数据库，查询最近 30 天的订单
```

**支持数据库**:
- SQLite（内置）
- PostgreSQL
- MySQL
- MongoDB

---

## 💡 使用技巧

### 1. 数据清洗
```
# 清理缺失值
"处理 DataFrame，填充缺失值为中位数"

# 去重
"移除重复的用户记录"
```

### 2. 数据分析
```
# 统计分析
"分析销售数据的趋势和季节性"

# 可视化
"生成月度销售额的折线图"
```

### 3. 数据转换
```
# 格式转换
"将 CSV 转换为 JSON 格式"

# 数据透视
"按部门和月份汇总员工绩效"
```

---

## 🔧 相关工具

衍智体提供以下数据处理工具：

| 工具名称 | 功能描述 |
|---------|---------|
| `file_read` | 读取文件内容 |
| `file_write` | 写入文件 |
| `bash` | 执行命令行工具 |
| `grep` | 搜索文本模式 |

---

## 📖 常用 Python 库

### 数据处理
```bash
# 安装依赖
pip install pandas numpy

# 基础用法
import pandas as pd
import numpy as np

# 读取数据
df = pd.read_csv('data.csv')

# 数据操作
df['total'] = df['quantity'] * df['price']
grouped = df.groupby('category')['total'].sum()

# 导出结果
df.to_excel('result.xlsx', index=False)
```

### 数据可视化
```bash
pip install matplotlib seaborn plotly

import matplotlib.pyplot as plt
import seaborn as sns

# 创建图表
plt.figure(figsize=(10, 6))
sns.barplot(data=df, x='category', y='total')
plt.title('销售额分类统计')
plt.savefig('chart.png', dpi=300)
plt.show()
```

---

## 🎯 实战案例

### 案例 1: 销售数据分析

```bash
# 步骤 1: 加载数据
yzt "读取 sales_2024.csv，显示前 10 行"

# 步骤 2: 数据清洗
yzt "清理数据：处理缺失值、异常值、重复记录"

# 步骤 3: 分析
yzt "按月份、产品类别分组统计销售额"

# 步骤 4: 可视化
yzt "生成年度销售趋势图和 Top 10 产品图表"

# 步骤 5: 报告
yzt "生成 Markdown 格式的分析报告"
```

### 案例 2: 日志分析

```bash
# 解析日志
yzt "解析 nginx access.log，提取访问量最高的页面"

# 统计分析
yzt "统计每小时请求量，找出高峰时段"

# 异常检测
yzt "识别异常的 HTTP 状态码和错误模式"
```

---

## ⚡ 性能优化建议

### 大文件处理
- 使用分块读取：`chunksize=10000`
- 选择合适的数据类型：`dtype={'id': 'int32'}`
- 避免循环：使用向量化操作

### 内存优化
- 只加载需要的列：`usecols=['A', 'B', 'C']`
- 使用分类类型：`astype('category')`
- 及时释放内存：`del df; gc.collect()`

---

**继续探索更多示例！**

[返回上级](../README.md) | [Web 开发](../web_development/README.md) | [自动化脚本](../automation/README.md)
