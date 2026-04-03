#!/usr/bin/env python3
"""
测试本地MLX模型运行
"""

import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "src"))

from yanzhiti.core.local_query_engine import LocalQueryEngine, LocalQueryEngineConfig
from yanzhiti.core import ToolRegistry
from yanzhiti.tools import (
    FileReadTool, GlobTool, GrepTool, BashTool,
    TaskCreateTool, TaskListTool, TodoWriteTool,
)


async def test_local_engine():
    """测试本地引擎"""
    print("=" * 70)
    print("Claude Code Local - MLX模型测试")
    print("=" * 70)
    print()

    # 创建工具注册表
    registry = ToolRegistry()
    registry.register(FileReadTool())
    registry.register(GlobTool())
    registry.register(GrepTool())
    registry.register(BashTool())
    registry.register(TaskCreateTool())
    registry.register(TaskListTool())
    registry.register(TodoWriteTool())

    print(f"✅ 已注册 {len(registry)} 个工具")
    print()

    # 创建配置 - 使用最小的模型进行测试
    config = LocalQueryEngineConfig(
        model_name="mlx-community/Llama-3.2-1B-Instruct-4bit",  # 最小模型
        max_tokens=512,  # 限制token数
        temperature=0.7,
        tools=registry.list_tools(),
        verbose=True,
    )

    print(f"📦 模型: {config.model_name}")
    print(f"📊 Max tokens: {config.max_tokens}")
    print()

    # 创建引擎
    print("🚀 初始化本地引擎...")
    engine = LocalQueryEngine(config)
    print()

    # 测试查询
    print("=" * 70)
    print("测试1: 简单查询")
    print("=" * 70)
    print()

    query1 = "你好，请介绍一下你自己"
    print(f"User: {query1}")
    print()

    try:
        response1 = await engine.query(query1)
        print(f"Assistant: {response1.content}")
        print()
    except Exception as e:
        print(f"❌ 错误: {e}")
        print("注意: 首次运行需要下载模型，可能需要几分钟时间")
        print()

    # 测试工具使用
    print("=" * 70)
    print("测试2: 工具使用")
    print("=" * 70)
    print()

    query2 = "列出当前目录的所有Markdown文件"
    print(f"User: {query2}")
    print()

    try:
        response2 = await engine.query(query2)
        print(f"Assistant: {response2.content}")
        print()
    except Exception as e:
        print(f"❌ 错误: {e}")
        print()

    # 显示统计
    print("=" * 70)
    print("会话统计")
    print("=" * 70)
    stats = engine.get_stats()
    print(f"Session ID: {stats['session_id']}")
    print(f"Messages: {stats['message_count']}")
    print(f"Turns: {stats['turn_count']}")
    print(f"Total tokens: {stats['usage']['total_tokens']}")
    print(f"Model: {stats['model']}")
    print()

    print("=" * 70)
    print("✅ 测试完成！")
    print("=" * 70)
    print()
    print("要使用完整功能，运行:")
    print("  claude-local")
    print()


if __name__ == "__main__":
    print()
    print("⚠️  注意: 首次运行会下载模型 (~700MB for 1B model)")
    print("   请确保有足够的磁盘空间和网络连接")
    print()
    print("按 Enter 继续，Ctrl+C 取消...")
    try:
        input()
        asyncio.run(test_local_engine())
    except KeyboardInterrupt:
        print("\n已取消")
