"""
Hugging Face Spaces 入口文件
这是部署到 Hugging Face Spaces 时使用的入口文件
"""
import os
import sys

# 确保可以导入项目模块
sys.path.insert(0, os.path.dirname(__file__))

# 导入主程序
from stock_query_assistant import app_gui

if __name__ == '__main__':
    # 启动Web界面
    app_gui()

