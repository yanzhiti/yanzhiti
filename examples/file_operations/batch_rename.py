"""
批量文件重命名工具
Batch File Rename Tool

使用衍智体生成的文件重命名工具
"""

import os
import sys
from pathlib import Path
from typing import List, Callable


def batch_rename(
    directory: str,
    pattern: str = "space_to_underscore",
    dry_run: bool = True
) -> List[dict]:
    """
    批量重命名文件
    
    参数:
        directory: 目标目录路径
        pattern: 重命名模式
                 - space_to_underscore: 空格转下划线
                 - to_lowercase: 转小写
                 - add_prefix: 添加前缀
                 - add_suffix: 添加后缀
                 - replace_text: 替换文本
        dry_run: 是否仅预览，不实际执行
        
    返回:
        重命名操作列表
    """
    dir_path = Path(directory)
    
    if not dir_path.exists():
        print(f"错误：目录 '{directory}' 不存在")
        return []
    
    if not dir_path.is_dir():
        print(f"错误：'{directory}' 不是目录")
        return []
    
    changes = []
    
    # 获取所有文件
    files = [f for f in dir_path.iterdir() if f.is_file()]
    
    for file_path in files:
        old_name = file_path.name
        new_name = apply_pattern(old_name, pattern)
        
        if old_name != new_name:
            changes.append({
                "old": str(file_path),
                "new": str(file_path.parent / new_name),
                "action": f"{old_name} → {new_name}"
            })
    
    # 显示预览
    print_preview(changes, dry_run)
    
    # 如果不只是预览，执行重命名
    if not dry_run and changes:
        confirm = input("\n确认执行这些重命名操作吗？(y/N): ")
        if confirm.lower() == 'y':
            execute_rename(changes)
            print(f"\n✅ 成功重命名 {len(changes)} 个文件")
        else:
            print("\n❌ 操作已取消")
    
    return changes


def apply_pattern(filename: str, pattern: str, **kwargs) -> str:
    """
    应用重命名模式
    
    参数:
        filename: 原文件名
        pattern: 模式名称
        **kwargs: 额外参数 (如 prefix, suffix, old_text, new_text)
        
    返回:
        新文件名
    """
    name, ext = os.path.splitext(filename)
    
    if pattern == "space_to_underscore":
        # 空格转下划线
        new_name = name.replace(" ", "_")
    
    elif pattern == "to_lowercase":
        # 转小写
        new_name = name.lower()
    
    elif pattern == "to_uppercase":
        # 转大写
        new_name = name.upper()
    
    elif pattern == "add_prefix":
        # 添加前缀
        prefix = kwargs.get("prefix", "")
        new_name = f"{prefix}{name}"
    
    elif pattern == "add_suffix":
        # 添加后缀
        suffix = kwargs.get("suffix", "")
        new_name = f"{name}{suffix}"
    
    elif pattern == "replace_text":
        # 替换文本
        old_text = kwargs.get("old_text", "")
        new_text = kwargs.get("new_text", "")
        new_name = name.replace(old_text, new_text)
    
    else:
        new_name = name
    
    return new_name + ext


def print_preview(changes: List[dict], dry_run: bool):
    """
    打印重命名预览
    
    参数:
        changes: 重命名操作列表
        dry_run: 是否仅预览模式
    """
    if not changes:
        print("\n没有需要重命名的文件")
        return
    
    print("\n" + "=" * 60)
    if dry_run:
        print("预览模式 (未实际执行):")
    else:
        print("将要执行的重命名操作:")
    print("=" * 60)
    
    for i, change in enumerate(changes, 1):
        print(f"{i:3d}. {change['action']}")
    
    print("=" * 60)
    print(f"共 {len(changes)} 个文件")


def execute_rename(changes: List[dict]):
    """
    执行重命名操作
    
    参数:
        changes: 重命名操作列表
    """
    for change in changes:
        try:
            os.rename(change["old"], change["new"])
            print(f"✓ {change['action']}")
        except Exception as e:
            print(f"✗ 重命名失败 {change['old']}: {e}")


def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(description="批量文件重命名工具")
    parser.add_argument(
        "directory",
        help="目标目录"
    )
    parser.add_argument(
        "-p", "--pattern",
        default="space_to_underscore",
        help="重命名模式 (space_to_underscore, to_lowercase, add_prefix, add_suffix, replace_text)"
    )
    parser.add_argument(
        "-e", "--execute",
        action="store_true",
        help="实际执行重命名 (默认仅预览)"
    )
    
    args = parser.parse_args()
    
    # 执行批量重命名
    batch_rename(args.directory, args.pattern, dry_run=not args.execute)


if __name__ == "__main__":
    main()
