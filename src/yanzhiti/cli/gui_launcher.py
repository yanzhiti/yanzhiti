"""
衍智体 (YANZHITI) 桌面客户端启动器
Desktop Client Launcher - Cross-platform desktop application

功能：
- 一键启动 Web GUI 界面
- 自动打开浏览器
- 系统托盘图标 (Windows/Mac)
- 自动检测可用端口
"""

import webbrowser


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

    return start_port


def launch_web_gui(port: int) -> None:
    """启动 Web GUI | Launch Web GUI"""
    import threading
    from urllib.request import urlopen

    # 启动 FastAPI 服务器 | Start FastAPI server
    def run_server():
        import uvicorn

        from yanzhiti.web.server import app
        uvicorn.run(app, host="0.0.0.0", port=port, log_level="warning")

    # 启动服务器线程 | Start server thread
    server_thread = threading.Thread(target=run_server, daemon=True)
    server_thread.start()

    # 等待服务器就绪 | Wait for server to be ready
    def wait_for_server():
        for _ in range(50):
            try:
                urlopen(f"http://127.0.0.1:{port}/health", timeout=1)
                return True
            except Exception:
                pass
        return False

    if not wait_for_server():
        print("错误：服务器启动失败 | Error: Server failed to start")
        return

    # 打开浏览器 | Open browser
    url = f"http://127.0.0.1:{port}"
    print(f"🌐 正在打开浏览器... | Opening browser at {url}")
    webbrowser.open(url)


def main():
    """主入口 | Main entry point"""
    import argparse

    parser = argparse.ArgumentParser(
        description="衍智体桌面客户端 | YANZHITI Desktop Client"
    )
    parser.add_argument(
        "--port", "-p", type=int, default=8080,
        help="端口 | Port (default: 8080)"
    )
    args = parser.parse_args()

    port = find_free_port(args.port)

    if port != args.port:
        print(f"⚠️  端口 {args.port} 已被占用，使用 {port} | Port {args.port} in use, using {port}")

    print("🚀 正在启动衍智体 Web GUI | Starting YANZHITI Web GUI...")
    launch_web_gui(port)


if __name__ == "__main__":
    main()
