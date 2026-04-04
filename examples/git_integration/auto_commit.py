"""
Git 自动提交工具
Git Auto Commit Tool

使用衍智体生成的 Git 自动化脚本
"""

import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import List, Tuple


def run_git_command(args: List[str]) -> Tuple[bool, str, str]:
    """
    运行 Git 命令
    
    参数:
        args: Git 命令参数列表
        
    返回:
        (成功标志，标准输出，标准错误)
    """
    try:
        result = subprocess.run(
            ["git"] + args,
            capture_output=True,
            text=True,
            check=False
        )
        return result.returncode == 0, result.stdout, result.stderr
    except Exception as e:
        return False, "", str(e)


def get_git_status() -> List[dict]:
    """
    获取 Git 状态信息
    
    返回:
        变更文件列表
    """
    success, stdout, stderr = run_git_command(["status", "--porcelain"])
    
    if not success:
        print(f"错误：无法获取 Git 状态 - {stderr}")
        return []
    
    changes = []
    for line in stdout.strip().split("\n"):
        if line:
            status = line[:2].strip()
            filename = line[3:]
            changes.append({
                "status": status,
                "filename": filename
            })
    
    return changes


def get_changed_files() -> Tuple[List[str], List[str]]:
    """
    获取变更文件列表
    
    返回:
        (新增/修改文件列表，删除文件列表)
    """
    changes = get_git_status()
    
    added_modified = []
    deleted = []
    
    for change in changes:
        status = change["status"]
        filename = change["filename"]
        
        if status.startswith("D"):
            deleted.append(filename)
        else:
            added_modified.append(filename)
    
    return added_modified, deleted


def generate_commit_message(files: List[str]) -> str:
    """
    自动生成提交信息
    
    参数:
        files: 变更文件列表
        
    返回:
        提交信息
    """
    if not files:
        return ""
    
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    
    # 统计文件类型
    file_types = {}
    for file in files:
        ext = Path(file).suffix.lower()
        file_types[ext] = file_types.get(ext, 0) + 1
    
    # 生成提交信息
    commit_msg = f"chore: 更新 {len(files)} 个文件\n\n"
    commit_msg += f"更新时间：{timestamp}\n\n"
    commit_msg += "变更文件:\n"
    
    # 按类型分组显示
    for ext, count in sorted(file_types.items()):
        ext_files = [f for f in files if Path(f).suffix.lower() == ext]
        if ext:
            commit_msg += f"- {ext} 文件 ({count}):\n"
            for f in ext_files[:5]:  # 最多显示 5 个
                commit_msg += f"  - {f}\n"
            if len(ext_files) > 5:
                commit_msg += f"  ... 还有 {len(ext_files) - 5} 个文件\n"
        else:
            commit_msg += f"- 无扩展名文件 ({count}):\n"
            for f in ext_files[:5]:
                commit_msg += f"  - {f}\n"
    
    return commit_msg


def auto_commit(dry_run: bool = True):
    """
    自动提交所有变更
    
    参数:
        dry_run: 是否仅预览，不实际执行
    """
    print("🔍 检查 Git 状态...")
    
    # 获取变更文件
    added_modified, deleted = get_changed_files()
    
    if not added_modified and not deleted:
        print("✅ 没有需要提交的变更")
        return
    
    print(f"\n📊 变更统计:")
    print(f"   新增/修改：{len(added_modified)} 个文件")
    print(f"   删除：{len(deleted)} 个文件")
    
    # 显示文件列表
    if added_modified:
        print(f"\n📝 新增/修改的文件:")
        for i, file in enumerate(added_modified[:10], 1):
            print(f"   {i:2d}. {file}")
        if len(added_modified) > 10:
            print(f"   ... 还有 {len(added_modified) - 10} 个文件")
    
    if deleted:
        print(f"\n🗑️  删除的文件:")
        for i, file in enumerate(deleted[:10], 1):
            print(f"   {i:2d}. {file}")
        if len(deleted) > 10:
            print(f"   ... 还有 {len(deleted) - 10} 个文件")
    
    # 生成提交信息
    all_files = added_modified + deleted
    commit_msg = generate_commit_message(all_files)
    
    print(f"\n📋 生成的提交信息:\n")
    print("-" * 60)
    print(commit_msg)
    print("-" * 60)
    
    if dry_run:
        print("\n💡 预览模式 - 未实际执行提交")
        print("   使用 --execute 参数来实际执行提交")
        return
    
    # 确认执行
    confirm = input("\n确认提交这些变更吗？(y/N): ")
    if confirm.lower() != 'y':
        print("❌ 操作已取消")
        return
    
    # 添加所有变更
    print("\n📦 添加所有变更...")
    success, stdout, stderr = run_git_command(["add", "-A"])
    if not success:
        print(f"❌ 添加失败：{stderr}")
        return
    print("✅ 添加成功")
    
    # 提交
    print("\n💾 提交变更...")
    success, stdout, stderr = run_git_command(["commit", "-m", commit_msg])
    if not success:
        print(f"❌ 提交失败：{stderr}")
        return
    
    print("✅ 提交成功!")
    
    # 显示提交信息
    success, stdout, stderr = run_git_command(["log", "-1", "--oneline"])
    if success:
        print(f"\n📌 最新提交：{stdout.strip()}")


def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Git 自动提交工具")
    parser.add_argument(
        "-e", "--execute",
        action="store_true",
        help="实际执行提交 (默认仅预览)"
    )
    
    args = parser.parse_args()
    
    auto_commit(dry_run=not args.execute)


if __name__ == "__main__":
    main()
