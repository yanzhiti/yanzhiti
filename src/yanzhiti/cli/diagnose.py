"""
错误诊断和自动修复工具
Error Diagnosis and Auto-Fix Tool
"""

import os
import platform
import subprocess
import sys
from pathlib import Path

import click
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Confirm
from rich.table import Table

console = Console()


class DiagnosticChecker:
    """诊断检查器 | Diagnostic checker"""

    def __init__(self):
        self.issues: list[dict] = []
        self.fixes: list[dict] = []

    def check_python_version(self) -> bool:
        """检查 Python 版本 | Check Python version"""
        console.print("\n[cyan]检查 Python 版本 | Checking Python version...[/cyan]")

        version = sys.version_info
        required = (3, 10)

        if version >= required:
            console.print(
                f"[green]✓ Python {version.major}.{version.minor}.{version.micro} (满足要求 | Required: 3.10+)[/green]"
            )
            return True
        else:
            error_msg = f"✗ Python {version.major}.{version.minor}.{version.micro} (需要 3.10+ | Required: 3.10+)"
            console.print(f"[red]{error_msg}[/red]")

            self.issues.append(
                {
                    "type": "python_version",
                    "severity": "error",
                    "message": error_msg,
                    "fix": "upgrade_python",
                }
            )
            return False

    def check_dependencies(self) -> bool:
        """检查依赖包 | Check dependencies"""
        console.print("\n[cyan]检查依赖包 | Checking dependencies...[/cyan]")

        required_packages = [
            "anthropic",
            "click",
            "rich",
            "pydantic",
            "httpx",
            "python-dotenv",
            "fastapi",
            "uvicorn",
        ]

        missing = []
        for pkg in required_packages:
            try:
                __import__(pkg.replace("-", "_"))
                console.print(f"[green]✓ {pkg}[/green]")
            except ImportError:
                console.print(f"[red]✗ {pkg} (缺失 | Missing)[/red]")
                missing.append(pkg)

        if missing:
            self.issues.append(
                {
                    "type": "missing_dependencies",
                    "severity": "error",
                    "message": f"Missing packages: {', '.join(missing)}",
                    "fix": "install_dependencies",
                    "packages": missing,
                }
            )
            return False

        console.print("[green]✓ 所有依赖已安装 | All dependencies installed[/green]")
        return True

    def check_env_file(self) -> bool:
        """检查 .env 文件 | Check .env file"""
        console.print("\n[cyan]检查配置文件 | Checking configuration file...[/cyan]")

        env_file = Path.cwd() / ".env"

        if not env_file.exists():
            console.print(f"[red]✗ .env file not found at {env_file}[/red]")
            self.issues.append(
                {
                    "type": "missing_env",
                    "severity": "error",
                    "message": "Configuration file (.env) not found",
                    "fix": "create_env",
                }
            )
            return False

        console.print(f"[green]✓ .env file exists: {env_file}[/green]")

        # 检查关键配置 | Check critical configs
        try:
            from dotenv import load_dotenv

            load_dotenv(env_file)

            api_key = os.getenv("YANZHITI_API_KEY")
            if not api_key:
                console.print("[red]✗ YANZHITI_API_KEY not set[/red]")
                self.issues.append(
                    {
                        "type": "missing_api_key",
                        "severity": "error",
                        "message": "API key not configured",
                        "fix": "configure_api_key",
                    }
                )
                return False

            console.print(
                f"[green]✓ API key configured (****{api_key[-4:] if len(api_key) > 4 else '****'})[/green]"
            )

            base_url = os.getenv("YANZHITI_BASE_URL")
            if base_url:
                console.print(f"[green]✓ Base URL: {base_url}[/green]")

            model = os.getenv("YANZHITI_MODEL")
            if model:
                console.print(f"[green]✓ Model: {model}[/green]")

            return True

        except Exception as e:
            console.print(f"[red]✗ Error reading .env: {e}[/red]")
            self.issues.append(
                {
                    "type": "env_read_error",
                    "severity": "error",
                    "message": f"Failed to read .env file: {e}",
                    "fix": "fix_env_file",
                }
            )
            return False

    def check_api_connection(self) -> bool:
        """检查 API 连接 | Check API connection"""
        console.print("\n[cyan]检查 API 连接 | Checking API connection...[/cyan]")

        try:
            import httpx
            from dotenv import load_dotenv

            load_dotenv()

            api_key = os.getenv("YANZHITI_API_KEY")
            base_url = os.getenv("YANZHITI_BASE_URL", "https://openrouter.ai/api/v1")

            if not api_key:
                console.print(
                    "[yellow]⚠ 跳过测试 (API key 未配置) | Skip test (no API key)[/yellow]"
                )
                return True

            import asyncio

            async def test():
                async with httpx.AsyncClient(timeout=10.0) as client:
                    headers = {"Authorization": f"Bearer {api_key}"}
                    response = await client.get(f"{base_url}/models", headers=headers)
                    return response.status_code in [200, 401, 403]

            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            success = loop.run_until_complete(test())

            if success:
                console.print("[green]✓ API connection successful[/green]")
                return True
            else:
                console.print("[red]✗ API connection failed[/red]")
                self.issues.append(
                    {
                        "type": "api_connection_error",
                        "severity": "warning",
                        "message": "Failed to connect to API",
                        "fix": "check_api_credentials",
                    }
                )
                return False

        except Exception as e:
            console.print(f"[red]✗ Connection error: {e}[/red]")
            self.issues.append(
                {
                    "type": "api_connection_error",
                    "severity": "error",
                    "message": f"API connection error: {e}",
                    "fix": "check_network",
                }
            )
            return False

    def check_permissions(self) -> bool:
        """检查文件权限 | Check file permissions"""
        console.print("\n[cyan]检查文件权限 | Checking file permissions...[/cyan]")

        # 检查当前目录是否可写 | Check if current directory is writable
        test_file = Path.cwd() / ".yanzhiti_test"
        try:
            test_file.touch()
            test_file.unlink()
            console.print("[green]✓ Write permissions OK[/green]")
            return True
        except Exception as e:
            console.print(f"[red]✗ Permission error: {e}[/red]")
            self.issues.append(
                {
                    "type": "permission_error",
                    "severity": "warning",
                    "message": f"Permission error: {e}",
                    "fix": "fix_permissions",
                }
            )
            return False

    def check_system_info(self) -> dict:
        """检查系统信息 | Check system information"""
        console.print("\n[cyan]系统信息 | System Information:[/cyan]")

        info = {
            "os": platform.system(),
            "os_version": platform.version(),
            "python_version": f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}",
            "platform": platform.platform(),
            "cwd": str(Path.cwd()),
        }

        table = Table(show_header=False)
        table.add_column("Key", style="cyan")
        table.add_column("Value", style="green")

        for key, value in info.items():
            table.add_row(key.replace("_", " ").title(), value)

        console.print(table)
        return info


def auto_fix(issue: dict) -> bool:
    """自动修复问题 | Auto-fix issue"""
    fix_type = issue.get("fix")

    if fix_type == "install_dependencies":
        packages = issue.get("packages", [])
        console.print(
            f"\n[cyan]正在安装缺失的依赖包 | Installing missing packages: {', '.join(packages)}[/cyan]"
        )

        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install"] + packages)
            console.print("[green]✓ 依赖包安装成功 | Dependencies installed successfully[/green]")
            return True
        except subprocess.CalledProcessError as e:
            console.print(f"[red]✗ 安装失败 | Installation failed: {e}[/red]")
            return False

    elif fix_type == "create_env":
        console.print("\n[cyan]创建 .env 文件 | Creating .env file...[/cyan]")

        env_content = """# YANZHITI Configuration
# Copy this file to .env and fill in your values

YANZHITI_API_KEY=your-api-key-here
YANZHITI_BASE_URL=https://openrouter.ai/api/v1
YANZHITI_MODEL=openai/gpt-3.5-turbo

# Model Parameters
YANZHITI_MAX_TOKENS=4096
YANZHITI_TEMPERATURE=1.0

# Execution Settings
YANZHITI_TIMEOUT=120
YANZHITI_MAX_RETRIES=3
YANZHITI_MAX_TURNS=100
"""

        env_file = Path.cwd() / ".env"
        try:
            with open(env_file, "w", encoding="utf-8") as f:
                f.write(env_content)

            console.print(f"[green]✓ .env file created: {env_file}[/green]")
            console.print(
                "[yellow]请编辑 .env 文件并填入您的 API 密钥 | Please edit .env file and add your API key[/yellow]"
            )
            return True
        except Exception as e:
            console.print(f"[red]✗ 创建失败 | Creation failed: {e}[/red]")
            return False

    elif fix_type == "upgrade_python":
        console.print("\n[yellow]请升级 Python 到 3.10 或更高版本[/yellow]")
        console.print("Please upgrade Python to 3.10 or higher")
        console.print("\n下载地址 | Download URL: https://www.python.org/downloads/")
        return False

    else:
        console.print(f"\n[yellow]⚠️  无法自动修复此问题 | Cannot auto-fix: {fix_type}[/yellow]")
        console.print(f"建议 | Suggestion: {issue.get('message')}")
        return False


def run_diagnosis(auto_fix_enabled: bool = False) -> tuple[bool, list[dict]]:
    """运行完整诊断 | Run full diagnosis"""
    console.print(
        Panel.fit(
            "[bold]衍智体 (YANZHITI) 诊断工具 | Diagnostic Tool[/bold]\n"
            "正在检查系统配置... | Checking system configuration...",
            style="cyan",
            border_style="green",
        )
    )

    checker = DiagnosticChecker()

    # 显示系统信息 | Show system info
    checker.check_system_info()

    # 执行检查 | Run checks
    checks = [
        ("Python 版本 | Python Version", checker.check_python_version),
        ("依赖包 | Dependencies", checker.check_dependencies),
        ("配置文件 | Configuration File", checker.check_env_file),
        ("API 连接 | API Connection", checker.check_api_connection),
        ("文件权限 | File Permissions", checker.check_permissions),
    ]

    results = []
    for name, check_func in checks:
        try:
            result = check_func()
            results.append((name, result))
        except Exception as e:
            console.print(f"[red]✗ {name}: Error - {e}[/red]")
            results.append((name, False))

    # 显示摘要 | Show summary
    console.print("\n" + "=" * 60)
    console.print("[bold]诊断摘要 | Diagnostic Summary[/bold]")
    console.print("=" * 60)

    passed = sum(1 for _, result in results if result)
    total = len(results)

    for name, result in results:
        status = "[green]✓ 通过 | Passed[/green]" if result else "[red]✗ 失败 | Failed[/red]"
        console.print(f"{status} - {name}")

    console.print(f"\n总计 | Total: {passed}/{total} 检查通过 | checks passed")

    # 显示问题列表 | Show issues
    if checker.issues:
        console.print(
            f"\n[bold red]发现 {len(checker.issues)} 个问题 | {len(checker.issues)} issues found:[/bold red]\n"
        )

        for i, issue in enumerate(checker.issues, 1):
            severity_icon = "🔴" if issue["severity"] == "error" else "🟡"
            console.print(f"{i}. {severity_icon} {issue['message']}")

            if (
                auto_fix_enabled
                and issue.get("fix")
                and Confirm.ask("   自动修复？| Auto-fix?", default=True)
            ):
                if auto_fix(issue):
                    console.print("   [green]✓ 修复成功 | Fixed successfully[/green]\n")
                else:
                    console.print("   [red]✗ 修复失败 | Fix failed[/red]\n")
    else:
        console.print("\n[bold green]✓ 未发现任何问题 | No issues found![/bold green]")

    all_passed = all(result for _, result in results)
    return all_passed, checker.issues


@click.command()
@click.option("--auto-fix", "-f", is_flag=True, help="自动修复问题 | Auto-fix issues")
@click.option("--verbose", "-v", is_flag=True, help="详细输出 | Verbose output")
def main(auto_fix: bool, verbose: bool):
    """
    诊断工具 - 检查并修复常见问题
    Diagnostic Tool - Check and fix common issues
    """
    try:
        success, issues = run_diagnosis(auto_fix_enabled=auto_fix)

        if success:
            console.print("\n[green]✓ 系统配置正常 | System configuration is OK[/green]\n")
            sys.exit(0)
        else:
            if not auto_fix and issues:
                console.print("\n[yellow]提示：使用 --auto-fix 选项自动修复问题[/yellow]")
                console.print("[yellow]Tip: Use --auto-fix option to auto-fix issues[/yellow]\n")
            sys.exit(1)

    except KeyboardInterrupt:
        console.print("\n\n[yellow]诊断已取消 | Diagnostic cancelled[/yellow]")
        sys.exit(0)
    except Exception as e:
        console.print(f"\n[red]诊断过程出错 | Diagnostic error: {e}[/red]")
        import traceback

        if verbose:
            traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
