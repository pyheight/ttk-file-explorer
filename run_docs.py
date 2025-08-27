#!/usr/bin/env python3

import os
import sys
import webbrowser
import subprocess

#os.environ['GIT_PYTHON_REFRESH'] = 'quiet'

class MkDocsManager:
    def __init__(self, quiet_mode=False):
        self.project_root = os.getcwd()
        self.mkdocs_process = None
        self.quiet_mode = quiet_mode

    def get_command(self, mode: str) -> list:
        """获取 MkDocs 命令"""
        cmd = ["mkdocs", mode]

        if self.quiet_mode:
            cmd.append("-q")

        if mode == "build":
            cmd.extend(["--clean", "--strict"])
        
        return cmd

    def run(self, mode: str = "serve") -> None:
        """启动 MkDocs 服务并处理相关操作"""
        print(f"项目路径: {self.project_root}")
        print(f"正在启动 MkDocs 服务 [模式: {mode}]...")

        cmd = self.get_command(mode)

        try:
            creation_flags = 0
            if sys.platform == "win32":
                creation_flags = subprocess.CREATE_NEW_PROCESS_GROUP

            self.mkdocs_process = subprocess.Popen(
                cmd,
                cwd=self.project_root,
                creationflags=creation_flags
            )

            if mode == "serve":
                url = "http://127.0.0.1:8000/"
                print(f"浏览器访问地址: {url}")
                webbrowser.open(url)
            
        except FileNotFoundError:
            print("\n未找到 MkDocs，请先安装: pip install -r docs/requirements.txt")
        except Exception as e:
            print(f"\n意外错误: {str(e)}")

if __name__ == "__main__":
    MkDocsManager().run()
