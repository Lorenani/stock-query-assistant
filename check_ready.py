#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
项目上传前检查脚本
检查项目是否准备好上传到GitHub
"""

import os
import re

def check_file_exists(filepath, description):
    """检查文件是否存在"""
    exists = os.path.exists(filepath)
    status = "✅" if exists else "❌"
    print(f"{status} {description}: {filepath}")
    return exists

def check_sensitive_info(filepath):
    """检查文件中是否包含敏感信息"""
    sensitive_patterns = [
        r'api[_-]?key\s*=\s*["\'][^"\']+["\']',
        r'password\s*=\s*["\'][^"\']+["\']',
        r'token\s*=\s*["\'][^"\']+["\']',
        r'secret\s*=\s*["\'][^"\']+["\']',
    ]
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read().lower()
            for pattern in sensitive_patterns:
                if re.search(pattern, content):
                    print(f"  ⚠️  警告: 发现可能的敏感信息模式: {pattern}")
                    return False
    except Exception as e:
        print(f"  ⚠️  无法读取文件: {e}")
    
    return True

def main():
    print("=" * 60)
    print("项目上传前检查")
    print("=" * 60)
    print()
    
    # 检查必需文件
    print("📁 检查必需文件:")
    print("-" * 60)
    files_to_check = [
        ("stock_query_assistant.py", "主程序文件"),
        ("requirements.txt", "依赖包列表"),
        ("README.md", "项目说明文档"),
        (".gitignore", "Git忽略文件"),
        ("faq.txt", "使用说明"),
    ]
    
    all_files_exist = True
    for filepath, description in files_to_check:
        if not check_file_exists(filepath, description):
            all_files_exist = False
    
    print()
    
    # 检查敏感信息
    print("🔒 检查敏感信息:")
    print("-" * 60)
    python_files = [f for f in os.listdir('.') if f.endswith('.py')]
    has_sensitive = False
    
    for py_file in python_files:
        if py_file == 'check_ready.py':
            continue
        print(f"检查 {py_file}...")
        if not check_sensitive_info(py_file):
            has_sensitive = True
    
    print()
    
    # 检查.gitignore
    print("📋 检查.gitignore配置:")
    print("-" * 60)
    if os.path.exists('.gitignore'):
        with open('.gitignore', 'r', encoding='utf-8') as f:
            gitignore_content = f.read()
            if '.env' in gitignore_content:
                print("✅ .env 已在.gitignore中")
            else:
                print("❌ .env 未在.gitignore中，建议添加")
            
            if '*.key' in gitignore_content:
                print("✅ *.key 已在.gitignore中")
            else:
                print("⚠️  *.key 未在.gitignore中，建议添加")
    else:
        print("❌ .gitignore 文件不存在")
    
    print()
    
    # 总结
    print("=" * 60)
    print("检查总结:")
    print("=" * 60)
    
    if all_files_exist:
        print("✅ 所有必需文件都存在")
    else:
        print("❌ 部分必需文件缺失，请补充")
    
    if not has_sensitive:
        print("✅ 未发现明显的敏感信息")
    else:
        print("⚠️  发现可能的敏感信息，请检查并移除")
    
    print()
    print("📝 下一步:")
    print("1. 如果所有检查都通过，可以开始上传到GitHub")
    print("2. 参考 GITHUB_GUIDE.md 了解详细的上传步骤")
    print("3. 确保API密钥等敏感信息使用环境变量，不要硬编码")
    print()

if __name__ == '__main__':
    main()

