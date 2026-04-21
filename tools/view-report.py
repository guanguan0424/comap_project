#!/usr/bin/env python3
"""
查看Allure测试报告的简单工具
"""

import os
import webbrowser
from http.server import HTTPServer, SimpleHTTPRequestHandler
import threading
import time

def start_server(port=8080, directory="allure-report"):
    """启动HTTP服务器"""
    os.chdir(directory)
    server = HTTPServer(('localhost', port), SimpleHTTPRequestHandler)
    print(f"🚀 Allure报告服务器启动在 http://localhost:{port}")
    print("按 Ctrl+C 停止服务器")
    
    # 在新线程中运行服务器
    server_thread = threading.Thread(target=server.serve_forever)
    server_thread.daemon = True
    server_thread.start()
    
    return server

def main():
    # 检查报告是否存在
    if not os.path.exists("allure-report"):
        print("❌ 未找到allure-report目录，请先生成报告")
        print("运行: allure generate allure-results -o allure-report --clean")
        return
    
    port = 8080
    
    # 启动服务器
    server = start_server(port)
    
    # 自动打开浏览器
    webbrowser.open(f"http://localhost:{port}")
    
    try:
        # 保持服务器运行
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n🛑 停止服务器")
        server.shutdown()

if __name__ == "__main__":
    main()