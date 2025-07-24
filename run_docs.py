#!/usr/bin/env python3
import os
import webbrowser
import subprocess


class MkDocsManager:
    def __init__(self):
        self.project_root = os.getcwd()

    def run(self, mode: str = "serve") -> None:
        """启动 MkDocs 服务并打开浏览器"""
        print(f"项目路径: {self.project_root}")
        print("启动 MkDocs 服务...")

        try:
            self.mkdocs_process = subprocess.Popen(
                ["mkdocs", mode],
                cwd=self.project_root,
                creationflags=subprocess.CREATE_NEW_PROCESS_GROUP
            )

            webbrowser.open("http://127.0.0.1:8000/")
            print("访问地址: http://127.0.0.1:8000/")

        except FileNotFoundError:
            print("未找到 MkDocs，请先安装 (pip install -r requirements_docs.txt)")


if __name__ == "__main__":
    MkDocsManager().run()
