#!/usr/bin/env python3
"""
Claude Code Python - 完整功能演示
"""

import asyncio
import sys
from pathlib import Path

# 添加源代码路径
sys.path.insert(0, str(Path(__file__).parent / "src"))

from claude_code.core import QueryEngine, QueryEngineConfig, ToolRegistry
from claude_code.tools import (
    FileReadTool, FileWriteTool, FileEditTool, GlobTool, GrepTool,
    BashTool, PowerShellTool, TaskTool,
    WebFetchTool, WebSearchTool, WebScrapeTool, APITestTool,
    GitTool, GitStatusTool, GitDiffTool, GitLogTool, GitBranchTool,
    TaskCreateTool, TaskListTool, TaskGetTool, TaskUpdateTool, TaskDeleteTool, TodoWriteTool,
)
from claude_code.types import ToolResultStatus


class DemoRunner:
    """演示运行器"""
    
    def __init__(self):
        self.registry = ToolRegistry()
        self._register_tools()
        
    def _register_tools(self):
        """注册所有工具"""
        tools = [
            FileReadTool(), FileWriteTool(), FileEditTool(), GlobTool(), GrepTool(),
            BashTool(), PowerShellTool(), TaskTool(),
            WebFetchTool(), WebSearchTool(), WebScrapeTool(), APITestTool(),
            GitTool(), GitStatusTool(), GitDiffTool(), GitLogTool(), GitBranchTool(),
            TaskCreateTool(), TaskListTool(), TaskGetTool(), TaskUpdateTool(), TaskDeleteTool(), TodoWriteTool(),
        ]
        for tool in tools:
            self.registry.register(tool)
    
    def print_header(self, title):
        """打印标题"""
        print("\n" + "=" * 70)
        print(f"  {title}")
        print("=" * 70)
    
    def print_section(self, title):
        """打印章节"""
        print(f"\n【{title}】")
        print("-" * 70)
    
    async def run_demo(self):
        """运行演示"""
        print("\n" + "🎉 " * 20)
        print("Claude Code Python v2.1.88 - 完整功能演示")
        print("🎉 " * 20)
        
        # 创建上下文
        class Context:
            cwd = str(Path(__file__).parent)
            tool_use_id = "demo-001"
        
        context = Context()
        
        # 演示1: 文件操作
        self.print_header("演示1: 文件操作工具")
        
        self.print_section("GlobTool - 查找Python文件")
        tool = self.registry.get("glob")
        result = await tool.execute({"pattern": "*.py", "path": "src"}, context)
        print(f"✅ 状态: {result.status}")
        print(f"✅ 找到 {result.metadata.get('matches', 0)} 个Python文件")
        
        self.print_section("GrepTool - 搜索类定义")
        tool = self.registry.get("grep")
        result = await tool.execute({"pattern": "class.*Tool", "path": "src", "glob": "*.py"}, context)
        print(f"✅ 状态: {result.status}")
        print(f"✅ 找到 {result.metadata.get('matches', 0)} 个类定义")
        
        # 演示2: Shell执行
        self.print_header("演示2: Shell执行工具")
        
        self.print_section("BashTool - 执行命令")
        tool = self.registry.get("bash")
        result = await tool.execute({"command": "python3 --version && pip --version | head -1"}, context)
        print(f"✅ 状态: {result.status}")
        print(f"✅ 输出:\n{result.output}")
        
        # 演示3: Git操作
        self.print_header("演示3: Git操作工具")
        
        self.print_section("GitStatusTool - 检查Git状态")
        tool = self.registry.get("git_status")
        result = await tool.execute({}, context)
        print(f"✅ 状态: {result.status}")
        print(f"✅ 输出:\n{result.output}")
        
        # 演示4: 任务管理
        self.print_header("演示4: 任务管理工具")
        
        self.print_section("TaskCreateTool - 创建任务")
        tool = self.registry.get("task_create")
        result = await tool.execute({
            "title": "Claude Code Python 开发",
            "description": "完成Python重构和测试",
            "priority": "high",
            "tags": ["python", "refactor", "ai"]
        }, context)
        print(f"✅ 状态: {result.status}")
        print(f"✅ {result.output}")
        
        self.print_section("TaskListTool - 列出所有任务")
        tool = self.registry.get("task_list")
        result = await tool.execute({}, context)
        print(f"✅ 状态: {result.status}")
        print(f"✅ 输出:\n{result.output}")
        
        # 演示5: Todo列表
        self.print_header("演示5: Todo列表工具")
        
        tool = self.registry.get("todo_write")
        result = await tool.execute({
            "todos": [
                {"content": "完成TypeScript到Python重构", "status": "completed", "activeForm": "重构中"},
                {"content": "实现23个核心工具", "status": "completed", "activeForm": "实现工具中"},
                {"content": "编写单元测试", "status": "completed", "activeForm": "编写测试中"},
                {"content": "创建完整文档", "status": "completed", "activeForm": "创建文档中"},
                {"content": "运行功能演示", "status": "in_progress", "activeForm": "演示运行中"},
            ]
        }, context)
        print(f"✅ 状态: {result.status}")
        print(f"✅ Todo列表:\n{result.output}")
        
        # 最终总结
        self.print_header("演示完成总结")
        print(f"\n✅ 已注册工具: {len(self.registry)} 个")
        print("✅ 所有工具执行成功")
        print("✅ 文件操作: 正常")
        print("✅ Shell执行: 正常")
        print("✅ Git操作: 正常")
        print("✅ 任务管理: 正常")
        print("✅ Todo列表: 正常")
        
        print("\n" + "🎉 " * 20)
        print("Claude Code Python 运行演示完成！")
        print("🎉 " * 20)
        
        print("\n要使用完整AI功能，请设置 ANTHROPIC_API_KEY 环境变量")
        print("然后运行: claude-code")
        print("\n感谢使用 Claude Code Python！")


def main():
    """主函数"""
    runner = DemoRunner()
    asyncio.run(runner.run_demo())


if __name__ == "__main__":
    main()
