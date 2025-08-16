#!/usr/bin/env python3

import os
import sys
import webbrowser
import subprocess


class MkDocsManager:
    def __init__(self):
        self.project_root = os.getcwd()
        self.mkdocs_process = None

    def run(self, mode: str = "serve") -> None:
        """启动 MkDocs 服务并处理相关操作"""
        print(f"项目路径: {self.project_root}")
        print(f"正在启动 MkDocs 服务 [模式: {mode}]...")
        
        try:
            creation_flags = 0
            if sys.platform == "win32":
                creation_flags = subprocess.CREATE_NEW_PROCESS_GROUP
            
            self.mkdocs_process = subprocess.Popen(
                ["mkdocs", mode],
                cwd=self.project_root,
                creationflags=creation_flags
            )
            
            # 仅 serve 模式需要打开浏览器
            if mode == "serve":
                url = "http://127.0.0.1:8000/"
                print(f"浏览器访问地址: {url}")
                webbrowser.open(url)
            
        except FileNotFoundError:
            print("\n未找到 MkDocs，请先安装: pip install -r requirements_docs.txt")
        except Exception as e:
            print(f"\n意外错误: {str(e)}")

if __name__ == "__main__":
    try:
        MkDocsManager().run()
    except KeyboardInterrupt:
        print("\n操作已由用户中断")
