"""
衍智体 (YANZHITI) 桌面客户端启动器
Desktop Client Launcher - Cross-platform desktop application

功能：
- 一键启动 Web GUI 界面
- 自动打开浏览器
- 系统托盘图标 (Windows/Mac)
- 自动检测可用端口
"""

import os
import sys
import webbrowser
from pathlib import Path


def find_free_port(start_port: int = 8080, max_tries: int = 10) -> int:
    """查找可用端口 | Find available port"""
    import socket
    
    for port in range(start_port, start_port + max_tries):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.bind(('127.0.0.1', port))
                return port
        except OSError:
            continue
    
    return start_port  # 如果都占用，返回默认端口


def launch_web_gui(port: int) -> None:
    """启动 Web GUI | Launch Web GUI"""
    import subprocess
    import threading
    from urllib.request import urlopen
    
    # 启动 FastAPI 服务器 | Start FastAPI server
    def run_server():
        import uvicorn
        uvicorn.run(
            "yanzhiti.web.server:app",
            host="127.0.0.1",
            port=port,
            log_level="info",
        )
    
    # 在后台线程中启动服务器 | Start server in background thread
    server_thread = threading.Thread(target=run_server, daemon=True)
    server_thread.start()
    
    # 等待服务器启动 | Wait for server to start
    import time
    print(f"正在启动服务器... | Starting server...")
    
    for i in range(30):  # 最多等待 3 秒
        try:
            urlopen(f"http://127.0.0.1:{port}/")
            break
        except Exception:
            time.sleep(0.1)
    else:
        print("❌ 服务器启动失败！| Server failed to start!")
        sys.exit(1)
    
    # 打开浏览器 | Open browser
    url = f"http://127.0.0.1:{port}"
    print(f"✅ 衍智体 Web GUI 已启动！")
    print(f"🌐 浏览器地址: {url}")
    print(f"\n按 Ctrl+C 停止服务 | Press Ctrl+C to stop")
    
    webbrowser.open(url)


def main():
    """主函数 | Main function"""
    print("=" * 60)
    print("🚀 衍智体 (YANZHITI) 桌面客户端 v2.1.88")
    print("=" * 60)
    
    # 查找可用端口 | Find available port
    port = find_free_port()
    
    # 显示启动信息 | Show startup info
    print(f"\n📁 工作目录: {os.getcwd()}")
    print(f"🔗 服务端口: {port}")
    print(f"🐍 Python 版本: {sys.version.split()[0]}")
    
    # 启动 Web GUI | Launch Web GUI
    launch_web_gui(port)


if __name__ == "__main__":
    main()
