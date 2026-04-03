#!/bin/bash

echo "========================================================================"
echo "衍智体 (YANZHITI) Local - 完整演示"
echo "========================================================================"
echo ""
echo "这个脚本将演示衍智体 (YANZHITI) Local的主要功能"
echo ""
echo "按Enter继续..."
read

source venv/bin/activate

echo ""
echo "1️⃣  检查MLX安装"
echo "------------------------------------------------------------------------"
python3 -c "import mlx; import mlx_lm; print('✅ MLX已安装')" || {
    echo "❌ MLX未安装，正在安装..."
    pip install mlx mlx-lm
}
echo ""

echo "2️⃣  检查命令"
echo "------------------------------------------------------------------------"
echo "✅ claude-local 版本:"
claude-local --version
echo ""

echo "3️⃣  可用选项"
echo "------------------------------------------------------------------------"
claude-local --help
echo ""

echo "4️⃣  工具演示"
echo "------------------------------------------------------------------------"
python3 << 'PYTHON'
import asyncio
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).parent / "src"))

from claude_code.core import ToolRegistry
from claude_code.tools import (
    FileReadTool, GlobTool, GrepTool, BashTool,
    GitStatusTool, TaskCreateTool, TodoWriteTool
)
from claude_code.core.tool import ToolContext

async def demo():
    registry = ToolRegistry()
    
    # 注册工具
    tools = [
        FileReadTool(), GlobTool(), GrepTool(), BashTool(),
        GitStatusTool(), TaskCreateTool(), TodoWriteTool()
    ]
    for tool in tools:
        registry.register(tool)
    
    print(f"已注册 {len(registry)} 个工具\n")
    
    context = ToolContext(cwd=".")
    
    # 演示1: Glob
    print("【演示1】GlobTool - 查找Python文件")
    result = await registry.get("glob").execute({"pattern": "*.py"}, context)
    print(f"找到 {result.metadata.get('matches', 0)} 个Python文件\n")
    
    # 演示2: Bash
    print("【演示2】BashTool - 执行命令")
    result = await registry.get("bash").execute({"command": "pwd && ls -la | head -5"}, context)
    print(f"{result.output[:200]}...\n")
    
    # 演示3: Task
    print("【演示3】TaskCreateTool - 创建任务")
    result = await registry.get("task_create").execute({
        "title": "衍智体 (YANZHITI) Local演示",
        "priority": "high"
    }, context)
    print(f"{result.output}\n")
    
    # 演示4: Todo
    print("【演示4】TodoWriteTool - Todo列表")
    result = await registry.get("todo_write").execute({
        "todos": [
            {"content": "安装MLX", "status": "completed", "activeForm": "安装中"},
            {"content": "运行演示", "status": "in_progress", "activeForm": "运行中"},
        ]
    }, context)
    print(f"{result.output}\n")

asyncio.run(demo())
PYTHON

echo ""
echo "========================================================================"
echo "✅ 演示完成！"
echo "========================================================================"
echo ""
echo "现在您可以:"
echo "  1. 运行交互模式: claude-local"
echo "  2. 单次查询: claude-local '您的问题'"
echo "  3. 指定模型: claude-local --model mlx-community/Llama-3.2-1B-Instruct-4bit"
echo ""
echo "首次使用会下载模型 (~700MB for 1B model)"
echo "模型下载后即可完全离线使用！"
echo ""
